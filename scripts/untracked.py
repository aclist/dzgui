import os
import subprocess
import sys

cmd = ["git", "ls-files", "--others", "--exclude-standard"]
result = subprocess.run(
    cmd, capture_output=True, text=True
)
untracked = [os.path.basename(line.rstrip()) for line in result.stdout.splitlines()]
if bool(untracked):
    print(f"The following files are untracked. Add to .gitignore if this is intended.")
    print("\n".join(untracked))
    sys.exit(1)
