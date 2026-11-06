import subprocess
from pathlib import Path

from dzgui.app_init import build_gui


def get_git_root() -> Path:
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True
    )
    if proc.returncode != 0:
        raise OSError("Failed to parse git root")
    return Path(proc.stdout.rstrip())


def get_image_path() -> Path:
    return get_git_root().joinpath("dzgui/data/images/example.png")


p = get_image_path()
app = build_gui("", False)
app.set_automation_param("screenshot_path", p)
app.run(None)
