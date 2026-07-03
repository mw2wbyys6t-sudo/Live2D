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

class PSDReader {
  private buf: Uint8Array;
  private view: DataView;

  constructor(buf: Uint8Array) {
    this.buf = buf;
    this.view = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  }

  readAscii(offset: number, length: number): string {
    let s = '';
    for (let i = 0; i < length; i++) {
      s += String.fromCharCode(this.buf[offset + i]);
    }
    return s;
  }

  readUInt8(offset: number): number {
    return this.view.getUint8(offset);
  }

  readUInt16BE(offset: number): number {
    return this.view.getUint16(offset);
  }

  readInt16BE(offset: number): number {
    return this.view.getInt16(offset);
  }

  readUInt32BE(offset: number): number {
    return this.view.getUint32(offset);
  }

  readInt32BE(offset: number): number {
    return this.view.getInt32(offset);
  }

  slice(start: number, end: number): Uint8Array {
    return this.buf.slice(start, end);
  }

  get length(): number {
    return this.buf.length;
  }

  getByte(offset: number): number {
    return this.buf[offset];
  }
}

function readPascalString(r: PSDReader, offset: number): { value: string; length: number } {
  const charCount = r.readUInt8(offset);
  let s = '';
  for (let i = 0; i < charCount; i++) {
    s += String.fromCharCode(r.getByte(offset + 1 + i));
  }
  const padded = ((charCount + 1 + 3) & ~3);
  return { value: s, length: padded };
}

function readUnicodeString(r: PSDReader, offset: number): { value: string; length: number } {
  const charCount = r.readUInt32BE(offset);
  const end = offset + 4 + charCount * 2;
  let s = '';
  for (let i = offset + 4; i < end; i += 2) {
    const code = (r.readUInt8(i) << 8) | r.readUInt8(i + 1);
    s += String.fromCharCode(code);
  }
  return { value: s, length: 4 + charCount * 2 };
}

function getColorModeName(mode: number): string {
  const modes: Record<number, string> = {
    0: 'Bitmap', 1: 'Grayscale', 2: 'Indexed', 3: 'RGB',
    4: 'CMYK', 5: 'Multi-channel', 6: 'Duotone', 7: 'Lab',
    8: '16-bit Grayscale', 9: '32-bit Grayscale', 10: '16-bit RGB', 11: '32-bit RGB',
  };
  return modes[mode] || `Unknown (${mode})`;
}

function parsePSDHeader(r: PSDReader): { width: number; height: number; depth: number; colorMode: number; offset: number } {
  const signature = r.readAscii(0, 4);
  const version = r.readUInt16BE(4);

  if (signature !== '8BPS') {
    throw new Error('Invalid PSD signature');
  }
  if (version !== 1) {
    throw new Error(`Unsupported PSD version: ${version}`);
  }

  const height = r.readUInt32BE(14);
  const width = r.readUInt32BE(18);
  const depth = r.readUInt16BE(22);
  const colorMode = r.readUInt16BE(24);

  return { width, height, depth, colorMode, offset: 26 };
}

function parsePSDLayers(r: PSDReader, startOffset: number): { layers: PSDLayer[]; groups: PSDGroup[]; offset: number } {
  const layers: PSDLayer[] = [];
  const groups: PSDGroup[] = [];
  let offset = startOffset;
  const groupStack: { name: string; id: string; index: number; depth: number }[] = [];
  let groupCount = 0;

  if (offset + 4 > r.length) {
    return { layers, groups, offset };
  }

  const layerInfoLength = r.readInt32BE(offset);
  offset += 4;

  const layerInfoEnd = offset + layerInfoLength;
  if (layerInfoEnd > r.length) {
    return { layers, groups, offset: r.length };
  }

  if (offset + 2 > r.length) {
    return { layers, groups, offset };
  }

  let layerCount = r.readInt16BE(offset);
  offset += 2;

  if (layerCount < 0) {
    layerCount = Math.abs(layerCount);
  }

  if (layerCount > 1000) {
    return { layers, groups, offset: layerInfoEnd };
  }

  for (let i = 0; i < layerCount; i++) {
    if (offset + 48 > r.length) break;

    const top = r.readInt32BE(offset); offset += 4;
    const left = r.readInt32BE(offset); offset += 4;
    const bottom = r.readInt32BE(offset); offset += 4;
    const right = r.readInt32BE(offset); offset += 4;

    const channelCount = r.readUInt16BE(offset); offset += 2;

    for (let c = 0; c < channelCount; c++) {
      offset += 6;
    }

    const blendSignature = r.readAscii(offset, 4);
    offset += 4;

    const blendMode = r.readAscii(offset, 4);
    offset += 4;

    const opacity = r.readUInt8(offset); offset += 1;
    const clipping = r.readUInt8(offset); offset += 1;
    const flags = r.readUInt8(offset); offset += 1;
    const filler = r.readUInt8(offset); offset += 1;

    const visible = !(flags & 0x02);

    const extraDataLength = r.readInt32BE(offset); offset += 4;
    const extraStart = offset;
    const extraEnd = offset + extraDataLength;

    let layerName = `Layer ${i}`;

    while (offset + 4 <= extraEnd) {
      const sig = r.readAscii(offset, 4);
      offset += 4;

      if (offset + 4 > extraEnd) break;
      const key = r.readAscii(offset, 4);
      offset += 4;

      if (offset + 4 > extraEnd) break;
      const dataLen = r.readInt32BE(offset);
      offset += 4;

      if (offset + dataLen > extraEnd) break;

      if (sig === '8BIM' && key === 'luni') {
        const result = readUnicodeString(r, offset);
        if (result.value) {
          layerName = result.value;
        }
      }

      offset += ((dataLen + 3) & ~3);
    }

    offset = extraEnd;

    const isGroupEnd = layerName === '</Layer group>';

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

export function parsePSD(data: ArrayBuffer | Uint8Array): PSDFileInfo {
  const buf = data instanceof Uint8Array ? data : new Uint8Array(data);
  const r = new PSDReader(buf);

  try {
    if (r.length < 26) {
      return {
        width: 0, height: 0, depth: 0, colorMode: 0,
        colorModeName: 'Unknown', layerCount: 0,
        layers: [], groups: [], valid: false,
        error: 'File too small to be a valid PSD',
      };
    }

    const header = parsePSDHeader(r);
    let offset = header.offset;

    const colorModeDataLength = r.readUInt32BE(offset);
    offset += 4 + colorModeDataLength;

    const imageResourcesLength = r.readUInt32BE(offset);
    offset += 4 + imageResourcesLength;

    const { layers, groups } = parsePSDLayers(r, offset);

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
    const msg = error instanceof Error ? error.message : String(error);
    return {
      width: 0, height: 0, depth: 0, colorMode: 0,
      colorModeName: 'Unknown', layerCount: 0,
      layers: [], groups: [], valid: false,
      error: msg || 'PSD解析失败',
    };
  }
}