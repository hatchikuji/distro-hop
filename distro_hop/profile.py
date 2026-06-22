# distro_hop/profile.py
from pathlib import Path
from datetime import datetime
import yaml


def export_profile(path: Path, distro: dict, packages: list[str], flatpak: list[str], snapcraft: list[str], dotfiles: list[str]) -> None:
    profile = {
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "distro": distro,
        },
        "packages": packages,
        "dotfiles": dotfiles,
        "flatpak": flatpak,
        "snapcraft": snapcraft
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(profile, f, allow_unicode=True, default_flow_style=False)


def load_profile(path: Path) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)
