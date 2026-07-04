const { parsePSD } = require('./dist/lib/psd-parser');
const { analyzePSD, getEnhancedResult } = require('./dist/lib/qa-engine');
const fs = require('fs');

const testPSD = fs.readFileSync('/tmp/test.psd');
const result = parsePSD(testPSD.buffer);

console.log('PSD Parse Result:');
console.log('- Valid:', result.valid);
console.log('- Width:', result.width);
console.log('- Height:', result.height);
console.log('- Layer Count:', result.layerCount);
console.log('- Layers:', result.layers.map(l => l.name));

if (result.valid) {
  const qaResult = analyzePSD(result);
  const enhanced = getEnhancedResult(qaResult);

  console.log('\nQA Result:');
  console.log('- Score:', enhanced.score);
  console.log('- Issues:', enhanced.issues.length);
  console.log('- Warnings:', enhanced.warnings.length);
  console.log('- Suggestions:', enhanced.suggestions.length);
}
