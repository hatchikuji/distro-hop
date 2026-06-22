# distro-hop

Sauvegarde et restaure ton environnement Linux quand tu changes de distro.

## Ce que ça fait

- Export des paquets installés (dnf, apt, pacman, zypper, apk...)
- Export des Flatpak
- Export des Snap
- Sauvegarde des dotfiles et configs (~/.config)
- Profil YAML versionnable et lisible

## Installation

```bash
git clone https://github.com/ton-pseudo/distro-hop
cd distro-hop
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

### Exporter l'environnement actuel

```bash
python -m distro_hop.cli export
```

Génère `profiles/fedora-44.yaml` (nommé automatiquement d'après la distro).

Tu peux aussi spécifier un chemin :

```bash
python -m distro_hop.cli export -o profiles/maconfig.yaml
```

### Afficher les infos d'un profil

```bash
python -m distro_hop.cli info
python -m distro_hop.cli info profiles/fedora-44.yaml
```

### Restaurer sur une nouvelle distro

```bash
python -m distro_hop.cli import profiles/fedora-44.yaml
```

## Structure du profil

```yaml
metadata:
  created_at: '2026-06-22T23:09:34'
  distro:
    id: fedora
    name: Fedora Linux
    version: '44'
    package_manager: dnf

packages:
  - firefox
  - git
  - vim
  ...

flatpaks:
  - com.spotify.Client
  - org.keepassxc.KeePassXC
  ...

dotfiles:
  - .bashrc
  - .gitconfig
  - .config/kdeglobals
  ...
```

## Distros supportées

Détection automatique du gestionnaire de paquets par binaire présent sur le système — pas de liste hardcodée. Fonctionne sur Fedora, Debian, Ubuntu, Arch, openSUSE, Void, Alpine, NixOS et toute distro avec un gestionnaire standard.

## Dépendances

Python 3.10+ · Typer · Rich · PyYAML