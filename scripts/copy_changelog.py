import shutil
import subprocess

from shared import get_git_root

root = get_git_root()
clog = root.joinpath("CHANGELOG.md")
target = root.joinpath("dzgui/data/CHANGELOG.md")

shutil.copy(clog, target)

subprocess.call(["git", "add", target])
