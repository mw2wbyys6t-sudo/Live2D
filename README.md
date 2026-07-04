# Live2D Master Agent v8.0

> **Professional AI-assisted Live2D production pipeline - from concept to rigging, ready for desktop deployment**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-v8.0.0-green.svg)]()
[![Tests](https://img.shields.io/badge/tests-149%20passed-brightgreen.svg)]()

---

## Quick Start (3 minutes)

```bash
# Install
python3 install.py

# Run pipeline with a local image
python3 live2d_workflow.py --input character.png --output ./output --k 5

# Generate from free AI (no API key needed)
python3 master_tool.py "anime girl with blue hair, white background"

# Deploy as desktop pet
python3 live2d_workflow.py --input character.png --output ./output --deploy-desktop
```

---

## What's New in v8.0 (Commercial Release)

**14 bugs fixed** across P0/P1/P2, **4 DEF features** implemented, full test coverage with 149 tests (all passing, zero API keys required).

### Bug Fixes
| Priority | Bug | Fix |
|----------|-----|-----|
| P0-1 | Version inconsistency (v7.2/v7.1/v3.0 scattered) | Single `live2d/version.py` source of truth |
| P0-2 | Tests require real API keys | All tests use mocks/synthetic images |
| P0-3 | Wrong default layerer (pro, not v6) | KMeansLayerer (v6) is default everywhere |
| P0-4 | XOR encryption fallback (security risk) | Fernet+PBKDF2 only; cryptography required |
| P0-5 | .env file path search broken | 7-location search algorithm |
| P1-1 | Circular imports between modules | Clean package architecture |
| P1-2 | Temporary file leaks | `finally` block cleanup; router removes failed outputs |
| P1-3 | Pet breaks when moved (relative paths) | `run_pet.py` uses `__file__` / `SCRIPT_DIR` |
| P1-4 | Go API fixed 60s timeout | Configurable `TimeoutSec` + `GetPythonTimeout()` |
| P2-1 | PSD zip bomb / malicious file risk | Magic bytes + dimension + layer count validation |
| P2-2 | QA/PSD issue IDs are random UUIDs | SHA256-based deterministic stable IDs |
| P2-3 | No `--version` flag on CLI tools | All 5 CLIs support `--version`/`-V` |
| P2-4 | `cryptography` missing from requirements | Added to requirements.txt and install.py |

### DEF Features
| DEF | Feature |
|-----|---------|
| DEF-003 | Seedream/Volcano ARK image generation provider |
| DEF-004 | 52-layer Cubism standard + physics3.json (22 params, 4 physics groups) |
| DEF-007 | Unified logging: Rich console + rotating file + sensitive data redaction |
| DEF-008 | `requirements-lock.txt` with pinned versions for reproducible builds |

---

## CLI Tools

| Command | Purpose |
|---------|---------|
| `python3 master_tool.py [prompt]` | Main entry: generate + layer + PSD + pet |
| `python3 live2d_workflow.py` | Full workflow engine (input image or prompt) |
| `python3 live2d_layer_v6.py` | K-means layer separation only |
| `python3 live2d_desktop_pet.py` | Desktop pet preview from layers directory |
| `python3 config_api.py` | Encrypted API key configuration |
| `python3 live2d_agent.py` | Interactive menu-driven agent |

All CLI tools support `--version` / `-V`.

### Key Options

```
--input PATH         Use existing character image (skip generation)
--output DIR         Output directory (default: ./output)
--k N                Number of K-means color clusters (3-20, default: 8)
--provider NAME      Image provider: pollinations (free, default) | sensenova | seedream
--deploy-desktop     Create desktop pet package after layering
--width / --height   Generation image dimensions (default: 512x512)
--seed N             Random seed for reproducible generations
```

---

## Pipeline Output

Running the workflow produces an output directory containing:

```
output/layers_<timestamp>/
  optimized_*.png         # Background-removed, enhanced source image
  layer_000.png ...       # K-means separated layer PNGs (RGBA)
  preview.png             # Layer preview composite
  LAYER_GUIDE.txt         # Layer color/component reference
  character.psd           # Multi-layer Adobe PSD file
  layer_mapping.json      # K-means cluster -> 52-layer standard mapping
  parameters.json         # 22 Cubism parameter definitions (ParamAngleX, etc.)
  physics3.json           # Physics configuration (HairFront, HairBack, BodyBounce, Breathing)
  52_LAYER_GUIDE.txt      # 52-layer standard reference
  pet_packages/<name>/    # Desktop pet package (with --deploy-desktop)
    run_pet.py            # Self-contained runner (uses __file__-relative paths)
    pet_config.json       # Animation configuration
    layers/               # Copied layer PNGs
```

---

## Configuration

Copy `.env.example` to `.env`:

```env
# Optional API keys (Pollinations works without a key)
SENSENOVA_API_KEY=sk-...
ARK_API_KEY=...

# Output
OUTPUT_DIR=./output

# Go API
GO_API_PORT=8080
GO_API_TIMEOUT_SEC=120

# Logging
LIVE2D_LOG_LEVEL=INFO
LIVE2D_TELEMETRY=0
```

The config searches 7 locations for `.env`: `LIVE2D_ENV_PATH`, `LIVE2D_PROJECT_ROOT/.env`, project root, CWD, script directory, `~/.trae-cn/skills/live2d-master-agent/.env`, `~/.live2d/.env`.

---

## Architecture

```
live2d/                          # Python package
  version.py                     # v8.0.0 (single source of truth)
  config.py                      # SecureConfig singleton (P0-5)
  logger.py                      # Unified logger (DEF-007)
  security.py                    # Path/PSD/prompt/filename validation
  secure_storage.py              # Fernet+PBKDF2 encrypted storage (P0-4)
  workflow.py                    # State machine engine (P1-2)
  image_gen/
    base.py                      # Abstract ImageProvider interface
    router.py                    # Provider registry with auto-fallback
    pollinations.py              # Free, no key required
    sensenova.py                 # SenseNova API
    seedream.py                  # Volcano ARK/Seedream (DEF-003)
  layering/
    kmeans.py                    # K-means v6 (DEFAULT, P0-3)
    layers52.py                  # 52-layer Cubism standard (DEF-004)
    part_identifier.py           # Color/position heuristic part detection
  psd/
    creator.py                   # PSD creation (psd-tools + PNG fallback)
    parser.py                    # PSD parser with bomb protection (P2-1)
    validator.py                 # PSD validator with stable IDs (P2-2)
  pet/
    animator.py                  # Pet package generator (P1-3 fix)
    runner.py                    # Direct pet preview
  qa/engine.py                   # QA scoring with stable hash IDs (P2-2)
api/                             # Go REST API (Gin framework)
  config/config.go               # Config struct + TimeoutSec (P1-4)
  services/python_bridge.go      # Defaults to live2d_layer_v6.py (P0-3)
  main.go                        # v8.0 version banner
tests/                           # 149 tests, zero API keys needed
  conftest.py                    # Fixtures: test_image, test_layers_dir, mock_requests
  test_workflow.py               # 67 unit tests
  test_full_coverage.py          # 49 edge case tests
  test_deep_coverage.py          # 33 integration/E2E tests
```

---

## Running Tests

```bash
# Run all tests (recommended):
python3 tests/test_workflow.py

# Run with pytest directly:
python3 -m pytest tests/ -v --tb=short

# Individual suites:
python3 -m pytest tests/test_workflow.py -v       # 67 unit tests
python3 -m pytest tests/test_full_coverage.py -v  # 49 edge case tests
python3 -m pytest tests/test_deep_coverage.py -v  # 33 integration/E2E tests
```

**All 149 tests pass without any external API keys or network access.**

---

## Security

- **Encryption**: Fernet (AES-128-CBC + HMAC-SHA256) with PBKDF2-HMAC-SHA256 (200,000 iterations); XOR fallback completely removed
- **Path traversal protection**: All paths validated; `..`, null bytes, dangerous characters blocked
- **PSD protection**: Magic byte check (`8BPS`), dimension limits (≤30000px), layer count limits before parsing
- **Prompt injection defense**: `rm -rf`, `;`, `&`, backticks, `eval`, `exec`, `system` patterns sanitized
- **Log redaction**: API keys (`sk-*`, Bearer tokens, JWTs) automatically redacted from logs and telemetry
- **File permissions**: Encrypted config stored with 0600 permissions; keys kept in memory only, not in `os.environ`

---

## Requirements

- Python 3.8+
- Core packages: Pillow, numpy, requests, psd-tools, scikit-learn, scipy, cryptography, rich
- Optional: pygame (desktop pet runtime, Python <3.14)
- Optional: Go 1.21+ (REST API server)

Install locked versions for reproducibility:
```bash
pip install -r requirements-lock.txt
```

---

## License

MIT
