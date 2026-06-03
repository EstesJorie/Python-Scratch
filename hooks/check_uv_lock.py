"""check uv.lock freshness"""

import subprocess
import sys


def check_uv_lock():
    """Check if uv.lock is up to date with pyproject.toml"""
    result = subprocess.run(["uv", "check"], capture_output=True, text=True)
    if result.returncode != 0:
        print("uv.lock is outdated. Running 'uv lock' to update it...")
        update_result = subprocess.run(["uv", "lock"], capture_output=True, text=True)
        if update_result.returncode != 0:
            print("Error: Failed to update uv.lock")
            print(update_result.stderr)
            sys.exit(1)
        else:
            print("uv.lock has been updated successfully.")
    else:
        print("uv.lock is up to date.")


if __name__ == "__main__":
    check_uv_lock()
