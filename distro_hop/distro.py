import platform
from pathlib import Path

def detect_distro() -> dict:
    info = {}
    os_release = Path("/etc/os-release")

    if os_release.exists():
        for line in os_release.read_text().splitlines():
            if "=" in line:
                key, _, value = line.partition("=")
                info[key] = value.strip('"')

    return {
        "id": info.get("ID", "unknown"),
        "name": info.get("NAME", "unknown"),
        "version": info.get("VERSION_ID", "unknown"),
        "package_manager": detect_package_manager("")
    }

def detect_package_manager(distro_id: str) -> str:
    # Essaie d'abord par le binaire présent sur le système
    managers = {
        "dnf": ["dnf"],
        "apt": ["apt"],
        "pacman": ["pacman"],
        "zypper": ["zypper"],
        "xbps": ["xbps-install"],  # Void Linux
        "emerge": ["emerge"],       # Gentoo
        "apk": ["apk"],             # Alpine
        "nix": ["nix"],             # NixOS
        "brew": ["brew"],           # macOS
    }

    import shutil
    for manager, binaries in managers.items():
        if all(shutil.which(b) for b in binaries):
            return manager

    return "unknown"
