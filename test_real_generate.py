#!/usr/bin/env python3
"""Real test of the workflow engine - generates a real image via Pollinations."""
import sys
import os
import json
import time
import shutil

sys.path.insert(0, '/workspace')
os.environ['PYTHONIOENCODING'] = 'utf-8'

from core.workflow import WorkflowEngine

OUTPUT_DIR = '/workspace/output/real_test'
if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"=== Real Generation Test ===")
print(f"Output dir: {OUTPUT_DIR}")
print(f"Provider: pollinations")
print()

engine = WorkflowEngine(
    output_dir=OUTPUT_DIR,
    provider='pollinations',
    width=512,
    height=768,
    use_semantic_segmentation=True,
    export_live2d=False,
    k_clusters=8
)

prompt = "1girl, blue hair, twin tails, school uniform, full body, standing, anime style, masterpiece, best quality, detailed background"
negative = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, cropped, worst quality, low quality"

print(f"Prompt: {prompt}")
print(f"Running full pipeline...")
print()

start = time.time()
try:
    result = engine.run(
        prompt=prompt,
        negative_prompt=negative,
        seed=42,
    )
    elapsed = time.time() - start
    print(f"\n=== Generation completed in {elapsed:.1f}s ===")
    print(f"Result keys: {list(result.keys()) if isinstance(result, dict) else 'not a dict'}")
    if isinstance(result, dict):
        for k, v in result.items():
            sv = str(v)[:200]
            print(f"  {k}: {sv}")
except Exception as e:
    elapsed = time.time() - start
    print(f"\n=== Failed after {elapsed:.1f}s: {type(e).__name__}: {e} ===")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Check generated artifacts
print(f"\n=== Artifacts in {OUTPUT_DIR} ===")
for root, dirs, files in os.walk(OUTPUT_DIR):
    for f in files:
        path = os.path.join(root, f)
        size = os.path.getsize(path)
        print(f"  {path}  ({size:,} bytes)")
