// @ts-check
const { parsePSD } = require('./lib/psd-parser');
const { analyzePSD, getEnhancedResult } = require('./lib/qa-engine');
const fs = require('fs');

// Create a minimal test PSD file
function createTestPSD() {
  // Minimal PSD structure: 8BPS signature + version (1) + reserved + dimensions + color mode + etc.
  const header = Buffer.alloc(26);
  header.write('8BPS', 0);           // Signature
  header.writeUInt16BE(1, 4);        // Version
  header.fill(0, 6, 14);            // Reserved
  header.writeUInt32BE(100, 14);    // Height
  header.writeUInt32BE(100, 18);    // Width
  header.writeUInt16BE(8, 22);      // Depth
  header.writeUInt16BE(3, 24);      // Color mode (RGB)

  // Add a layer record
  const layerCount = Buffer.alloc(4);
  layerCount.writeInt32BE(2, 0); // 2 layers

  return Buffer.concat([header, layerCount]);
}

// Test
console.log('Testing PSD Parser...');
try {
  const testData = createTestPSD();
  const result = parsePSD(testData.buffer);
  console.log('Parse Result:', result);

  if (result.valid) {
    const qaResult = analyzePSD(result);
    const enhanced = getEnhancedResult(qaResult);
    console.log('QA Score:', enhanced.score);
    console.log('Issues:', enhanced.issues.length);
  }
  console.log('Test PASSED!');
} catch (e) {
  console.error('Test FAILED:', e);
}
