import subprocess
from pathlib import Path

from dzgui.app_init import build_gui
from shared import get_git_root


def get_image_path() -> Path:
    return get_git_root().joinpath("dzgui/data/images/example.png")


p = get_image_path()
app = build_gui("", False)
app.set_automation_param("screenshot_path", p)
app.run(None)
