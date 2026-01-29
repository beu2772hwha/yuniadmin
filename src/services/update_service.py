from __future__ import annotations

import json
import os
import shutil
import tempfile
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from src.config import get_data_dir
from src.version import __version__

REPO = "beu2772hwha/yuniadmin"
API_URL = f"https://api.github.com/repos/{REPO}/releases/latest"


@dataclass
class ReleaseInfo:
    version: str
    zip_url: str


def _parse_version(raw: str) -> tuple[int, int, int]:
    value = raw.strip().lstrip("v")
    parts = value.split(".")
    major = int(parts[0]) if len(parts) > 0 else 0
    minor = int(parts[1]) if len(parts) > 1 else 0
    patch = int(parts[2]) if len(parts) > 2 else 0
    return major, minor, patch


def _is_newer(current: str, latest: str) -> bool:
    return _parse_version(latest) > _parse_version(current)


def get_latest_release() -> Optional[ReleaseInfo]:
    try:
        with urllib.request.urlopen(API_URL, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception:
        return None

    tag_name = data.get("tag_name")
    if not tag_name:
        return None

    assets = data.get("assets", [])
    zip_asset = next((a for a in assets if a.get("name", "").endswith(".zip")), None)
    if not zip_asset:
        return None

    return ReleaseInfo(version=tag_name, zip_url=zip_asset.get("browser_download_url"))


def download_and_extract(zip_url: str) -> Path:
    data_dir = get_data_dir()
    temp_dir = Path(tempfile.mkdtemp(prefix="update_", dir=data_dir))
    zip_path = temp_dir / "release.zip"

    with urllib.request.urlopen(zip_url, timeout=30) as response:
        with open(zip_path, "wb") as file:
            shutil.copyfileobj(response, file)

    extract_dir = temp_dir / "extracted"
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)

    return extract_dir


def check_for_update() -> Optional[ReleaseInfo]:
    release = get_latest_release()
    if not release:
        return None
    if not _is_newer(__version__, release.version):
        return None
    return release


def prepare_update() -> Optional[Path]:
    release = check_for_update()
    if not release:
        return None
    return download_and_extract(release.zip_url)


def get_app_root() -> Path:
    return Path(__file__).resolve().parents[2]
