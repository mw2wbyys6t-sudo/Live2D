export interface PSDFileInfo {
  width: number;
  height: number;
  depth: number;
  colorMode: number;
  colorModeName: string;
  layerCount: number;
  layers: PSDLayer[];
  groups: PSDGroup[];
  valid: boolean;
  error?: string;
}

export interface PSDLayer {
  index: number;
  name: string;
  visible: boolean;
  opacity: number;
  blendMode: string;
  bounds: {
    top: number;
    left: number;
    bottom: number;
    right: number;
    width: number;
    height: number;
  };
  isGroup: boolean;
  groupId: string | null;
  isGroupEnd: boolean;
  channels: number;
  hasImageData: boolean;
  flags: {
    transparencyProtected: boolean;
    visible: boolean;
    obsolete: boolean;
    pixelDataIrrelevant: boolean;
  };
  depth: number;
}

export interface PSDGroup {
  id: string;
  name: string;
  layerIndex: number;
  layerIds: number[];
  depth: number;
}

function readPascalString(buf: Buffer, offset: number): { value: string; length: number } {
  const charCount = buf.readUInt8(offset);
  const str = buf.toString('utf8', offset + 1, offset + 1 + charCount);
  const padded = ((charCount + 1 + 3) & ~3);
  return { value: str, length: padded };
}

function readUnicodeString(buf: Buffer, offset: number): { value: string; length: number } {
  const charCount = buf.readUInt32BE(offset);
  const end = offset + 4 + charCount * 2;
  const raw = buf.subarray(offset + 4, end);
  const codeUnits: number[] = [];
  for (let i = 0; i < raw.length; i += 2) {
    codeUnits.push((raw[i] << 8) | raw[i + 1]);
  }
  const str = String.fromCharCode(...codeUnits);
  return { value: str, length: 4 + charCount * 2 };
}

function getColorModeName(mode: number): string {
  const modes: Record<number, string> = {
    0: 'Bitmap',
    1: 'Grayscale',
    2: 'Indexed',
    3: 'RGB',
    4: 'CMYK',
    5: 'Multi-channel',
    6: 'Duotone',
    7: 'Lab',
    8: '16-bit Grayscale',
    9: '32-bit Grayscale',
    10: '16-bit RGB',
    11: '32-bit RGB',
  };
  return modes[mode] || `Unknown (${mode})`;
}

function parsePSDHeader(buf: Buffer): { width: number; height: number; depth: number; colorMode: number; offset: number } {
  const signature = buf.toString('ascii', 0, 4);
  const version = buf.readUInt16BE(4);

  if (signature !== '8BPS') {
    throw new Error('Invalid PSD signature');
  }
  if (version !== 1) {
    throw new Error(`Unsupported PSD version: ${version}`);
  }

  const channels = buf.readUInt16BE(12);
  const height = buf.readUInt32BE(14);
  const width = buf.readUInt32BE(18);
  const depth = buf.readUInt16BE(22);
  const colorMode = buf.readUInt16BE(24);

  return { width, height, depth, colorMode, offset: 26 };
}

function parsePSDLayers(buf: Buffer, startOffset: number): { layers: PSDLayer[]; groups: PSDGroup[]; offset: number } {
  const layers: PSDLayer[] = [];
  const groups: PSDGroup[] = [];
  let offset = startOffset;
  const groupStack: { name: string; id: string; index: number; depth: number }[] = [];
  let groupCount = 0;

  if (offset + 4 > buf.length) {
    return { layers, groups, offset };
  }

  const layerInfoLength = buf.readInt32BE(offset);
  offset += 4;

  const layerInfoEnd = offset + layerInfoLength;
  if (layerInfoEnd > buf.length) {
    return { layers, groups, offset: buf.length };
  }

  if (offset + 2 > buf.length) {
    return { layers, groups, offset };
  }

  let layerCount = buf.readInt16BE(offset);
  offset += 2;

  if (layerCount < 0) {
    layerCount = Math.abs(layerCount);
  }

  if (layerCount > 1000) {
    return { layers, groups, offset: layerInfoEnd };
  }

  const layerRecords: { offset: number; size: number }[] = [];

  for (let i = 0; i < layerCount; i++) {
    if (offset + 48 > buf.length) break;

    const recordStart = offset;

    const top = buf.readInt32BE(offset); offset += 4;
    const left = buf.readInt32BE(offset); offset += 4;
    const bottom = buf.readInt32BE(offset); offset += 4;
    const right = buf.readInt32BE(offset); offset += 4;

    const channelCount = buf.readUInt16BE(offset); offset += 2;

    for (let c = 0; c < channelCount; c++) {
      offset += 6;
    }

    const blendSignature = buf.toString('ascii', offset, offset + 4);
    offset += 4;

    const blendMode = buf.toString('ascii', offset, offset + 4);
    offset += 4;

    const opacity = buf.readUInt8(offset); offset += 1;
    const clipping = buf.readUInt8(offset); offset += 1;
    const flags = buf.readUInt8(offset); offset += 1;
    const filler = buf.readUInt8(offset); offset += 1;

    const visible = !(flags & 0x02);

    const extraDataLength = buf.readInt32BE(offset); offset += 4;
    const extraStart = offset;
    const extraEnd = offset + extraDataLength;

    let layerName = `Layer ${i}`;

    while (offset + 4 <= extraEnd) {
      const sig = buf.toString('ascii', offset, offset + 4);
      offset += 4;

      if (offset + 4 > extraEnd) break;
      const key = buf.toString('ascii', offset, offset + 4);
      offset += 4;

      if (offset + 4 > extraEnd) break;
      const dataLen = buf.readInt32BE(offset);
      offset += 4;

      if (offset + dataLen > extraEnd) break;

      if (sig === '8BIM' && key === 'luni') {
        const result = readUnicodeString(buf, offset);
        if (result.value) {
          layerName = result.value;
        }
      } else if (sig === '8BIM' && key === 'lsct') {
        // Section divider setting
      }

      offset += ((dataLen + 3) & ~3);
    }

    offset = extraEnd;

    const isGroupStart = layerName === '</Layer group>' || layerName.startsWith('</L');
    const isGroupEnd = layerName === '</Layer group>' || layerName.startsWith('</L');

    let actualIsGroup = false;
    let actualGroupId: string | null = null;

    if (layerName.startsWith('<')) {
      if (layerName === '</Layer group>') {
        if (groupStack.length > 0) {
          groupStack.pop();
        }
      } else if (layerName.startsWith('<L')) {
        groupCount++;
        const groupId = `group_${groupCount}`;
        groupStack.push({ name: layerName.replace(/[<>]/g, '').trim(), id: groupId, index: i, depth: groupStack.length });
        actualIsGroup = true;
        actualGroupId = groupId;
      }
    } else {
      actualGroupId = groupStack.length > 0 ? groupStack[groupStack.length - 1].id : null;
    }

    const layer: PSDLayer = {
      index: i,
      name: layerName,
      visible,
      opacity: opacity / 255,
      blendMode,
      bounds: {
        top, left, bottom, right,
        width: Math.max(0, right - left),
        height: Math.max(0, bottom - top),
      },
      isGroup: actualIsGroup,
      groupId: actualGroupId,
      isGroupEnd: isGroupEnd,
      channels: channelCount,
      hasImageData: channelCount > 0 && !isGroupEnd,
      flags: {
        transparencyProtected: !!(flags & 0x01),
        visible: !(flags & 0x02),
        obsolete: !!(flags & 0x04),
        pixelDataIrrelevant: !!(flags & 0x10),
      },
      depth: groupStack.length,
    };

    layers.push(layer);
    layerRecords.push({ offset: recordStart, size: offset - recordStart });
  }

  const activeGroups = groupStack.map(g => ({
    id: g.id,
    name: g.name,
    layerIndex: g.index,
    layerIds: layers
      .filter(l => l.groupId === g.id && !l.isGroup && !l.isGroupEnd)
      .map(l => l.index),
    depth: g.depth,
  }));

  return { layers, groups: activeGroups, offset };
}

export function parsePSD(buffer: Buffer): PSDFileInfo {
  try {
    if (buffer.length < 26) {
      return {
        width: 0, height: 0, depth: 0, colorMode: 0,
        colorModeName: 'Unknown', layerCount: 0,
        layers: [], groups: [], valid: false,
        error: 'File too small to be a valid PSD',
      };
    }

    const header = parsePSDHeader(buffer);
    let offset = header.offset;

    const colorModeDataLength = buffer.readUInt32BE(offset);
    offset += 4 + colorModeDataLength;

    const imageResourcesLength = buffer.readUInt32BE(offset);
    offset += 4 + imageResourcesLength;

    const { layers, groups } = parsePSDLayers(buffer, offset);

    const displayLayers = layers.filter(l => !l.name.startsWith('<'));

    return {
      width: header.width,
      height: header.height,
      depth: header.depth,
      colorMode: header.colorMode,
      colorModeName: getColorModeName(header.colorMode),
      layerCount: displayLayers.length,
      layers: displayLayers,
      groups,
      valid: true,
    };
  } catch (error: any) {
    return {
      width: 0, height: 0, depth: 0, colorMode: 0,
      colorModeName: 'Unknown', layerCount: 0,
      layers: [], groups: [], valid: false,
      error: error.message,
    };
  }
}