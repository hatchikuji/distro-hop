# distro_hop/cli.py
import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from distro_hop.distro import detect_distro
from distro_hop.packages import get_installed_packages, get_installed_flatpak, get_installed_snap
from distro_hop.dotfiles import get_existing_dotfiles, export_dotfiles
from distro_hop.profile import export_profile, load_profile

app = typer.Typer(help="Gestionnaire de distro hopping")
console = Console()

@app.command()
@app.command()
def export(
        output: Path = typer.Option(None, "--output", "-o", help="Fichier de sortie"),
        dotfiles_dir: Path = typer.Option(Path("profiles/dotfiles"), "--dotfiles-dir", "-d", help="Dossier dotfiles"),
):
    """Exporte l'environnement actuel dans un profil."""
    distro = detect_distro()

    if output is None:
        output = Path(f"profiles/{distro['id']}-{distro['version']}.yaml")
    """Exporte l'environnement actuel dans un profil."""
    console.print("[bold green]Détection de la distro...[/bold green]")
    console.print(f"  Distro : [cyan]{distro['name']} {distro['version']}[/cyan]")
    console.print(f"  Gestionnaire : [cyan]{distro['package_manager']}[/cyan]")

    console.print("[bold green]Export des paquets...[/bold green]")
    packages = get_installed_packages(distro["package_manager"])
    console.print(f"  {len(packages)} paquets trouvés")
    flatpak = get_installed_flatpak()
    console.print(f"  {len(flatpak)} Flatpak trouvés")
    snapcraft = get_installed_snap()
    console.print(f"  {len(snapcraft)} Snap trouvés")

    console.print("[bold green]Export des dotfiles...[/bold green]")
    dotfiles = get_existing_dotfiles()
    copied = export_dotfiles(dotfiles_dir)
    console.print(f"  {len(copied)} dotfiles copiés")

    export_profile(output, distro, packages, flatpak, snapcraft, dotfiles)
    console.print(f"\n[bold]Profil sauvegardé dans[/bold] [cyan]{output}[/cyan]")


@app.command()
def info(
        profile: Path = typer.Argument(None, help="Profil à afficher"),
):
    """Affiche les infos d'un profil."""
    if profile is None:
        distro = detect_distro()
        profile = Path(f"profiles/{distro['id']}-{distro['version']}.yaml")
    data = load_profile(profile)
    meta = data["metadata"]

    table = Table(title="Profil distro-hop")
    table.add_column("Clé", style="cyan")
    table.add_column("Valeur")

    table.add_row("Distro", f"{meta['distro']['name']} {meta['distro']['version']}")
    table.add_row("Créé le", meta["created_at"])
    table.add_row("Paquets", str(len(data["packages"])))
    table.add_row("Flatpak", str(len(data["flatpak"])))
    table.add_row("Snapcraft", str(len(data["snapcraft"])))
    table.add_row("Dotfiles", str(len(data["dotfiles"])))
    console.print(table)


if __name__ == "__main__":
    app()