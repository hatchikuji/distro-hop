# distro_hop/packages.py
import subprocess
from typing import Optional

def get_installed_packages(package_manager: str) -> list[str]:
    commands = {
        "dnf": ["rpm", "-qa", "--queryformat", "%{NAME}\n"],
        "apt": ["apt-mark", "showmanual"],
        "pacman": ["pacman", "-Qqe"],
        "zypper": ["zypper", "search", "--installed-only", "--type", "package", "-x"],
    }

    cmd = commands.get(package_manager)
    if not cmd:
        raise ValueError(f"Gestionnaire de paquets non supporté : {package_manager}")

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    packages = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return sorted(packages)

def install_packages(packages: list[str], package_manager: str) -> None:
    commands = {
        "dnf": ["sudo", "dnf", "install", "-y"],
        "apt": ["sudo", "apt", "install", "-y"],
        "pacman": ["sudo", "pacman", "-S", "--noconfirm"],
        "zypper": ["sudo", "zypper", "install", "-y"],
    }

    cmd = commands.get(package_manager)
    if not cmd:
        raise ValueError(f"Gestionnaire de paquets non supporté : {package_manager}")

    subprocess.run(cmd + packages, check=True)

def get_installed_flatpak() -> list[str]:
        try:
            result = subprocess.run(
                ["flatpak", "list", "--app", "--columns=application"],
                capture_output=True, text=True, check=True
            )
            return sorted([line.strip() for line in result.stdout.splitlines() if line.strip()])
        except (subprocess.CalledProcessError, FileNotFoundError):
            return []


def install_flatpak(flatpak: list[str]) -> None:
    if not flatpak:
        return
    subprocess.run(
        ["flatpak", "install", "--noninteractive", "flathub"] + flatpak,
        check=True
    )

def get_installed_snap() -> list[str]:
    try:
        result = subprocess.run(
            ["snap", "list", "--columns=name"],
            capture_output=True, text=True, check=True
        )
        return sorted([line.strip() for line in result.stdout.splitlines() if line.strip()])
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []

def install_snap(snapcraft: list[str]) -> None:
    if not snapcraft:
        return
    subprocess.run(
        ["snap", "install", "--noninteractive", "snapcraft"] + snapcraft,
        check=True
    )