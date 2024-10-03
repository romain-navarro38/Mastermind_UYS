from dataclasses import dataclass
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent


@dataclass
class Dir:
    ROOT = ROOT_DIR
    HTML = ROOT_DIR / "resource" / "html"
    ICON = ROOT_DIR / "resource" / "icons"
    STYLE = ROOT_DIR / "resource" / "styles"


def get_resource(filename: Path) -> str:
    """Retourne le contenu de la ressource située au chemin donné"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()
