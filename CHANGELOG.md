# Changelog

## v8.0.0 - Commercial Release (2026-07-02)

This is the commercial v8.0 release. All 14 documented P0-P2 bugs are fixed.
Four DEF feature requirements are fully implemented. The entire test suite
(149 tests) passes without requiring any external API keys.

### Breaking Changes

- New Python package architecture: `live2d/` replaces the old `exec()` wrapper pattern.
  All entry points now use proper `import live2d.*` statements.
- XOR encryption fallback completely removed; `cryptography` package is now required.
- Default layerer is KMeans (v6), not layer_pro. Go API bridge defaults to `live2d_layer_v6.py`.
- Config singleton must be reset between tests (handled by `reset_config` fixture).

### P0 Bug Fixes (Critical)

- **P0-1 Version Inconsistency**: Created `live2d/version.py` as the single source of
  truth (`__version__ = "8.0.0"`). Added `VERSION` file at project root. All other
  version references import from this module. Test `test_all_version_references_are_v8`
  verifies no stale v7.x references remain in Python source.
- **P0-2 Tests Require API Keys**: All 149 tests use synthetic PIL-generated test images
  and mocked HTTP requests (`mock_requests` fixture monkeypatches `requests.get/post`).
  No network calls are made during testing.
- **P0-3 Wrong Default Layerer**: `WorkflowEngine` uses `KMeansLayerer` (v6) as default.
  Go API `python_bridge.go` defaults to `live2d_layer_v6.py`. `master_tool.py` calls
  KMeans v6 directly after generation.
- **P0-4 XOR Encryption Fallback**: Removed `_simple_encrypt`/`_simple_decrypt` methods
  entirely. `SecureStorage` requires the `cryptography` package (raises `ImportError`
  with clear message if missing). Uses Fernet (AES-128-CBC + HMAC-SHA256) with
  PBKDF2-HMAC-SHA256 key derivation (200,000 iterations).
- **P0-5 .env Path Resolution**: `SecureConfig._find_env_file()` searches 7 locations:
  `LIVE2D_ENV_PATH`, `LIVE2D_PROJECT_ROOT/.env`, project root, CWD, script directory,
  `~/.trae-cn/skills/live2d-master-agent/.env`, `~/.live2d/.env`.

### P1 Bug Fixes (High)

- **P1-1 Circular Imports**: Eliminated by proper package architecture with explicit
  imports and lazy loading for heavy modules (sklearn, psd_tools, pygame) via
  `live2d/__init__.py` `__getattr__()`.
- **P1-2 Temp File Leaks**: `WorkflowEngine._track_temp()` / `_cleanup_temp()` in a
  `finally` block guarantees cleanup. `ProviderRouter` removes partially-written output
  files on generation failure.
- **P1-3 Pet Relative Path Bug**: Generated `run_pet.py` uses
  `SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))` and `os.chdir(SCRIPT_DIR)`
  so the pet package works from any working directory.
- **P1-4 Go API Fixed Timeout**: Added `TimeoutSec int` field to `PythonConfig` struct
  in Go. Added `Config.GetPythonTimeout() time.Duration` method. Python bridge uses
  dynamic timeout instead of hardcoded value. Default timeout increased from 60s to 120s.

### P2 Bug Fixes (Medium)

- **P2-1 PSD Malicious File Protection**: `validate_psd_file()` checks magic bytes
  (`8BPS`), version, channel count (1-56), dimensions (≤30000px), bit depth, color mode,
  and file size (≤500MB). `scan_psd_layer_count()` limits layers before full parsing.
  `PSDParser.parse()` validates before parsing and raises `PSDValidationError`.
- **P2-2 Stable QA/PSD Issue IDs**: QA engine generates deterministic issue IDs via
  `SHA256("{code}:{context}")[:10]` → `"QA-{hash}"` format. PSD parser uses stable IDs
  via `SHA256("name|ox,oy|wxh")[:12]` → `"LAYER-{hash}"` format. PSD validator uses
  fixed code strings (E001-E005, W001-W003, I001).
- **P2-3 --version Flags**: All 5 CLI entry points (`master_tool.py`, `live2d_workflow.py`,
  `live2d_layer_v6.py`, `live2d_desktop_pet.py`, `config_api.py`) support `--version`/`-V`.
- **P2-4 cryptography in Requirements**: Added `cryptography>=41.0.0` to `requirements.txt`
  and to `CORE_DEPS` in `install.py`. Added installation verification step to install.py.

### DEF Features Implemented

- **DEF-003 Seedream/ARK Provider**: Full `SeedreamProvider` implementation supporting
  seedream-3.0/4.0/5.0 models with size mapping (512-2048px), async task polling, and
  OpenAI-compatible `/images/generations` endpoint. Registered in provider router with
  highest priority when `ARK_API_KEY` is set.
- **DEF-004 52-Layer Standard**: Complete `LIVE2D_52_LAYERS` (52 entries from Background
  to Hair_Highlight_Front in back-to-front draw order), `STANDARD_PARAMS` (22 parameters
  including ParamAngleX/Y/Z, ParamEyeLOpen/ROpen, ParamMouthOpenY, etc.), and
  `STANDARD_PHYSICS` (physics3.json version 3 with 4 physics groups: HairFront, HairBack,
  BodyBounce, Breathing). Generates `layer_mapping.json`, `parameters.json`,
  `physics3.json`, and `52_LAYER_GUIDE.txt`.
- **DEF-007 Unified Logging**: `Live2DLogger` class with Rich console handler (when
  available) and rotating file handler. Automatic sensitive data redaction for
  api_key/secret/password/token fields. Opt-in telemetry system (via `LIVE2D_TELEMETRY=1`)
  with JSONL flush. Pipeline step progress via `step()` and `section()` methods.
  Singleton factory `get_logger(name)`.
- **DEF-008 Dependency Lock File**: Created `requirements-lock.txt` with pinned versions
  for all core dependencies (Pillow==10.4.0, numpy==1.26.4, scipy==1.13.1,
  scikit-learn==1.5.1, psd-tools==1.9.28, cryptography==42.0.8, etc.).

### Other Improvements

- **Go API**: CORS is configurable via `AllowedOrigins` (defaults to `["*"]` for dev).
  `WriteTimeout` increased to 180s for image generation. BaseDir path resolution fixed.
- **Security**: Prompt sanitization blocks command injection patterns (`rm -rf`, `;`, `&`,
  backticks, `eval`/`exec`/`system`). Filename sanitization removes dangerous characters.
  `redact_sensitive()` masks `sk-*` keys, Bearer tokens, and JWTs in logs.
- **Install**: `install.py` includes `--check` flag for verifying installed packages.
  Creates `.env.example` and output directory automatically.
- **Background Removal**: Smooth alpha ramp at background color boundary for cleaner edges
  (fixed numpy scalar conversion bug).
- **Pet Package**: Generates `run_pet.py`, `run_pet.bat`, `run_pet.sh` (chmod 755),
  `README.txt`, and `pet_config.json` in addition to layer copies.

### Test Results

- **test_workflow.py**: 67 tests - all passing
- **test_full_coverage.py**: 49 tests - all passing
- **test_deep_coverage.py**: 33 tests - all passing
- **Total**: 149 tests passing, 0 failures, 0 skipped
- **API keys required**: None (all HTTP mocked, all images synthetic)
- **External network calls**: None during test execution

### Files Created/Modified

New files created (v8.0):
- `live2d/__init__.py`, `live2d/version.py`, `live2d/logger.py`, `live2d/security.py`,
  `live2d/secure_storage.py`, `live2d/config.py`, `live2d/workflow.py`
- `live2d/image_gen/__init__.py`, `base.py`, `pollinations.py`, `sensenova.py`,
  `seedream.py`, `router.py`
- `live2d/layering/__init__.py`, `kmeans.py`, `layers52.py`, `part_identifier.py`
- `live2d/psd/__init__.py`, `creator.py`, `parser.py`, `validator.py`
- `live2d/pet/__init__.py`, `animator.py`, `runner.py`
- `live2d/qa/__init__.py`, `engine.py`
- `tests/__init__.py`, `tests/conftest.py`, `tests/test_workflow.py`,
  `tests/test_full_coverage.py`, `tests/test_deep_coverage.py`
- `requirements-lock.txt`, `VERSION`, `.env.example`

Files rewritten (v8.0):
- `master_tool.py`, `live2d_workflow.py`, `live2d_layer_v6.py`, `live2d_layer_pro.py`,
  `live2d_desktop_pet.py`, `config_api.py`, `live2d_agent.py`, `install.py`,
  `requirements.txt`, `README.md`

Files modified (v8.0):
- `api/config/config.go`, `api/services/python_bridge.go`, `api/main.go`

---

## Earlier versions

See git history for v7.x changelog entries.
