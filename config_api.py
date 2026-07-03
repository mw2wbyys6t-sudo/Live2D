#!/usr/bin/env python3
"""
Live2D Master Agent v8.0 - API Configuration Tool
Interactive setup for API keys (stored encrypted with Fernet/PBKDF2).
"""

import os
import sys
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

_PROJECT_ROOT = str(Path(__file__).resolve().parent)
os.environ.setdefault("LIVE2D_PROJECT_ROOT", _PROJECT_ROOT)
sys.path.insert(0, _PROJECT_ROOT)


def main():
    from live2d.version import FULL_VERSION_STRING
    from live2d.config import config
    from live2d.secure_storage import _CRYPTO_AVAILABLE

    print(f"\n{FULL_VERSION_STRING}")
    print("=" * 50)
    print("API Key Configuration")
    print("=" * 50)

    if not _CRYPTO_AVAILABLE:
        print("\n[ERROR] cryptography package required. Run: pip install cryptography")
        print("        python install.py")
        sys.exit(1)

    print(f"\nCurrent status:")
    print(f"  SenseNova API key: {'***' + config.sensenova_api_key[-4:] if config.sensenova_api_key else 'NOT SET'}")
    print(f"  ARK/Seedream API key: {'***' + config.ark_api_key[-4:] if config.ark_api_key else 'NOT SET'}")
    print(f"  Free provider (Pollinations.ai): Always available")
    print(f"  Output directory: {config.output_dir}")

    print("\n" + "-" * 50)
    print("1. Set SenseNova API key")
    print("2. Set ARK/Seedream API key")
    print("3. Set output directory")
    print("4. Show .env file location")
    print("5. Clear all keys")
    print("0. Exit")
    print("-" * 50)

    choice = input("\nSelect option [0-5]: ").strip()

    if choice == "1":
        key = input("Enter SenseNova API key (sk-...): ").strip()
        if key:
            config.set("SENSENOVA_API_KEY", key, persist=True)
            print(f"[OK] SenseNova API key saved (encrypted)")
        else:
            print("Cancelled.")
    elif choice == "2":
        key = input("Enter ARK/Seedream API key: ").strip()
        if key:
            config.set("ARK_API_KEY", key, persist=True)
            print(f"[OK] ARK/Seedream API key saved (encrypted)")
        else:
            print("Cancelled.")
    elif choice == "3":
        d = input(f"Enter output directory [{config.output_dir}]: ").strip()
        if d:
            config.set("OUTPUT_DIR", d)
            # Also write to .env
            env_path = Path(_PROJECT_ROOT) / ".env"
            content = ""
            if env_path.exists():
                content = env_path.read_text(encoding="utf-8")
            # Update OUTPUT_DIR line
            import re
            if re.search(r'^OUTPUT_DIR=', content, re.MULTILINE):
                content = re.sub(r'^OUTPUT_DIR=.*$', f'OUTPUT_DIR={d}', content, flags=re.MULTILINE)
            else:
                content += f"\nOUTPUT_DIR={d}\n"
            env_path.write_text(content, encoding="utf-8")
            print(f"[OK] Output directory set to: {d}")
    elif choice == "4":
        env_paths = [
            Path(_PROJECT_ROOT) / ".env",
            Path(_PROJECT_ROOT) / ".env.encrypted",
        ]
        print("\nConfig files:")
        for p in env_paths:
            exists = "EXISTS" if p.exists() else "not found"
            print(f"  {p}: {exists}")
    elif choice == "5":
        confirm = input("Are you sure you want to clear all keys? [yes/NO]: ").strip().lower()
        if confirm == "yes":
            enc_file = Path(_PROJECT_ROOT) / ".env.encrypted"
            if enc_file.exists():
                enc_file.unlink()
            print("[OK] All encrypted keys removed.")
        else:
            print("Cancelled.")
    elif choice == "0":
        print("Goodbye!")
    else:
        print("Invalid option.")

    print(f"\nDone. Free generation via Pollinations.ai works without any API keys.")


if __name__ == "__main__":
    main()
