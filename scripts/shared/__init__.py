import subprocess
from pathlib import Path


def get_git_root() -> Path:
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True
    )
    if proc.returncode != 0:
        raise OSError("Failed to parse git root")
    return Path(proc.stdout.rstrip())
