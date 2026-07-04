function writeString(bytes: Uint8Array, offset: number, str: string): void {
  for (let i = 0; i < str.length; i++) {
    bytes[offset + i] = str.charCodeAt(i);
  }
}

export function createPSDFromImage(
  imageData: ImageData,
  width: number,
  height: number,
  layerName: string = 'Image'
): ArrayBuffer {
  const channels = 3
  const headerSize = 26
  const colorModeDataSize = 4
  const pixelCount = width * height

  const resData = new ArrayBuffer(28)
  const resView = new DataView(resData)
  const resBytes = new Uint8Array(resData)
  let ro = 0
  writeString(resBytes, ro, '8BIM'); ro += 4
  resView.setUint16(ro, 0x03ED); ro += 2
  resView.setUint16(ro, 0); ro += 2
  resView.setUint32(ro, 16); ro += 4
  resView.setUint32(ro, 72 << 16); ro += 4
  resView.setUint16(ro, 1); ro += 2
  resView.setUint16(ro, 1); ro += 2
  resView.setUint32(ro, 72 << 16); ro += 4
  resView.setUint16(ro, 1); ro += 2
  resView.setUint16(ro, 2); ro += 2

  const imageResourcesSize = 4 + resData.byteLength

  const nameBytes = 4 + layerName.length * 2
  const namePadded = ((nameBytes + 3) & ~3)
  const luniBlockSize = 4 + 4 + 4 + namePadded
  const extraDataSize = ((luniBlockSize + 3) & ~3)
  const layerRecordSize = 4 * 4 + 2 + channels * 6 + 4 + 4 + 1 + 1 + 1 + 1 + 4 + extraDataSize
  const channelDataSize = channels * (2 + pixelCount)
  const layerInfoBodySize = 2 + layerRecordSize + channelDataSize
  const layerAndMaskSize = 4 + layerInfoBodySize + 4

  const compositeDataSize = 2 + pixelCount * 3

  const totalSize = headerSize + colorModeDataSize + imageResourcesSize + layerAndMaskSize + compositeDataSize

  const buffer = new ArrayBuffer(totalSize)
  const bytes = new Uint8Array(buffer)
  const view = new DataView(buffer)

  let o = 0

  writeString(bytes, o, '8BPS'); o += 4
  view.setUint16(o, 1); o += 2
  o += 6
  view.setUint16(o, 3); o += 2
  view.setUint32(o, height); o += 4
  view.setUint32(o, width); o += 4
  view.setUint16(o, 8); o += 2
  view.setUint16(o, 3); o += 2

  view.setUint32(o, 0); o += 4

  const resSectionLenPos = o
  view.setUint32(o, resData.byteLength); o += 4
  bytes.set(new Uint8Array(resData), o); o += resData.byteLength

  const layerInfoLenPos = o
  view.setUint32(o, 0); o += 4

  view.setInt16(o, 1); o += 2

  view.setInt32(o, 0); o += 4
  view.setInt32(o, 0); o += 4
  view.setInt32(o, height); o += 4
  view.setInt32(o, width); o += 4

  view.setUint16(o, channels); o += 2

  const channelInfoPositions: number[] = []
  for (let c = 0; c < channels; c++) {
    view.setInt16(o, c); o += 2
    channelInfoPositions.push(o)
    view.setUint32(o, 0); o += 4
  }

  writeString(bytes, o, '8BIM'); o += 4
  writeString(bytes, o, 'norm'); o += 4

  view.setUint8(o, 255); o += 1
  view.setUint8(o, 0); o += 1
  view.setUint8(o, 0); o += 1
  view.setUint8(o, 0); o += 1

  const extraDataLenPos = o
  view.setUint32(o, 0); o += 4
  const extraDataStart = o

  writeString(bytes, o, '8BIM'); o += 4
  writeString(bytes, o, 'luni'); o += 4

  const luniDataLenPos = o
  view.setUint32(o, 0); o += 4
  const luniDataStart = o

  view.setUint32(o, layerName.length); o += 4
  for (let i = 0; i < layerName.length; i++) {
    view.setUint16(o, layerName.charCodeAt(i)); o += 2
  }

  const luniDataLen = o - luniDataStart
  view.setUint32(luniDataLenPos, luniDataLen)

  const extraDataLen = o - extraDataStart
  const extraDataPadded = ((extraDataLen + 3) & ~3)
  while (o - extraDataStart < extraDataPadded) {
    view.setUint8(o, 0); o += 1
  }
  view.setUint32(extraDataLenPos, o - extraDataStart)

  for (let c = 0; c < channels; c++) {
    const channelStart = o
    view.setUint16(o, 0); o += 2
    const srcOffset = c
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        bytes[o] = imageData.data[(y * width + x) * 4 + srcOffset]
        o++
      }
    }
    view.setUint32(channelInfoPositions[c], o - channelStart)
  }

  view.setUint32(layerInfoLenPos, o - (layerInfoLenPos + 4))

  view.setUint32(o, 0); o += 4

  view.setUint16(o, 0); o += 2

  for (let c = 0; c < 3; c++) {
    const srcOffset = c
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        bytes[o] = imageData.data[(y * width + x) * 4 + srcOffset]
        o++
      }
    }
  }

  return buffer
}