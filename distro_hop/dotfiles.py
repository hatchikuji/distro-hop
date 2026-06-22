# distro_hop/dotfiles.py
from pathlib import Path

COMMON_DOTFILES = [
    ".bashrc",
    ".bash_profile",
    ".zshrc",
    ".profile",
    ".gitconfig",
    ".vimrc",
    ".tmux.conf",
    ".ssh/config",
]

COMMON_CONFIG_DIRS = [
    # KDE Plasma
    ".config/kdeglobals",
    ".config/kwinrc",
    ".config/kwinoutputconfig.json",
    ".config/konsolerc",
    ".config/dolphinrc",
    ".config/kglobalshortcutsrc",
    ".config/plasma-org.kde.plasma.desktop-appletsrc",
    ".config/plasmashellrc",
    ".config/plasmarc",
    ".config/kscreenlockerrc",
    ".config/kdeconnect",
    ".config/gtk-3.0",
    ".config/gtk-4.0",
    ".config/autostart",
    # Apps
    ".config/mpv",
    ".config/fastfetch",
    ".config/rclone",
    ".config/qBittorrent",
    ".config/vlc",
    # Dev
    ".config/JetBrains",
    ".config/github-copilot",
]

def get_existing_dotfiles(home: Path = None) -> list[str]:
    if home is None:
        home = Path.home()

    found = []

    for f in COMMON_DOTFILES + COMMON_CONFIG_DIRS:
        p = home / f
        if p.exists():
            found.append(str(p.relative_to(home)))

    return found


def export_dotfiles(dest: Path, home: Path = None) -> list[str]:
    import shutil
    if home is None:
        home = Path.home()

    dest.mkdir(parents=True, exist_ok=True)
    copied = []

    for f in get_existing_dotfiles(home):
        src = home / f
        dst = dest / f
        dst.parent.mkdir(parents=True, exist_ok=True)

        try:
            if src.is_dir():
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst, ignore_dangling_symlinks=True)
            else:
                shutil.copy2(src, dst)
            copied.append(f)
        except Exception as e:
            print(f"  [warn] ignoré {f} : {e}")

    return copied