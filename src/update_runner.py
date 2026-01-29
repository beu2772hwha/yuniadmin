from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path

SKIP_DIRS = {".git", ".venv", "data", "__pycache__"}


def _copy_tree(src: Path, dst: Path) -> None:
    for item in src.iterdir():
        if item.name in SKIP_DIRS:
            continue
        target = dst / item.name
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            _copy_tree(item, target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def main() -> None:
    if len(sys.argv) < 3:
        return
    extracted_dir = Path(sys.argv[1]).resolve()
    app_root = Path(sys.argv[2]).resolve()

    time.sleep(2)

    root_candidate = extracted_dir
    if (extracted_dir / "src").exists():
        root_candidate = extracted_dir
    else:
        for child in extracted_dir.iterdir():
            if child.is_dir() and (child / "src").exists():
                root_candidate = child
                break

    _copy_tree(root_candidate, app_root)

    python_exe = sys.executable
    subprocess.Popen([python_exe, "-m", "src.app"], cwd=str(app_root))


if __name__ == "__main__":
    main()
