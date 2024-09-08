from enum import Enum, StrEnum, auto
from pathlib import Path
from typing import Self

RESOURCE_DIR = Path(__file__).parent.parent.parent / "resource"
ICON_DIR = RESOURCE_DIR / "icons"
STYLE_DIR = RESOURCE_DIR / "styles"
HTML_DIR = RESOURCE_DIR / "html"
SIZE_COMBINATION = 4
SQUARE = "\u25A0"  # correspondant à ■
DOT = "\u25CF"  # correspondant à ●
RESET_COLOR = "\033[0m"
PREAMBLE = """{start_h1}JEU DU MASTERMIND{end_h1}
{start_paragraph}Trouver la bonne combinaison de {SIZE_COMBINATION} couleurs secrètes que notre 'IA' aura générée.{return_line}
A chaque couleur bien positionnée, vous aurez en retour un indicateur rouge.{return_line}
A chaque couleur présente mais mal positionnée, vous aurez en retour un indicateur blanc.{end_paragraph}"""


class Color(StrEnum):
    """Classe StrEnum représentant une couleur
    associé à son code hexadécimal"""
    JAUNE = '#ffff00'
    BLEU = '#0000ff'
    ROUGE = '#ff0000'
    VERT = '#00ff00'
    BLANC = '#ffffff'
    MAGENTA = '#ff00ff'
    CYAN = '#00ffff'
    MARRON = '#906434'
    NOIR = "#000000"
    GRIS = '#7f7f7f'

    def to_rgb(self) -> tuple[int, int, int]:
        """Retourne la couleur au format RGB"""
        return (int(self.value[i:i + 2], 16) for i in range(1, len(self.value), 2))

    @classmethod
    def from_index(cls, index: int) -> Self:
        return list(cls)[index]

    def get_opposite(self) -> str:
        """Retourne la couleur opposée au format hexadécimal"""
        return f"#{''.join([f'{hex(255 - c)[2:]:02}' for c in self.to_rgb()])}"


class Level(Enum):
    """Classe Enum représentant le nombre de couleurs disponible
    pour composer une combinaison"""
    FACILE = 4
    NORMAL = 6
    DIFFICILE = 8

    def __str__(self):
        return self.name.lower()

    @classmethod
    def from_string(cls, name: str) -> Self:
        return next(attribute for attribute in cls if attribute.name.lower() == name)

    @classmethod
    def to_list(cls) -> list[str]:
        return list(str(attribute) for attribute in cls)


class Neighbor(Enum):
    """Classe Enum représentant le pion voisin,
    à droite ou à gauche, dans une ligne d'essai"""
    RIGHT = auto()
    LEFT = auto()


class Try(Enum):
    """Classe Enum représentant le nombre maximum d'essais
    pour trouver la combinaison secrète"""
    FACILE = 12
    NORMAL = 10

    def __str__(self):
        return self.name.lower()

    @classmethod
    def from_string(cls, name: str) -> Self:
        return next(attribute for attribute in cls if attribute.name.lower() == name)

    @classmethod
    def to_list(cls) -> list[str]:
        return list(str(attribute) for attribute in cls)


class View(StrEnum):
    """Classe Enum représentant une vue"""
    CONSOLE = 'console'
    WINDOW = 'fenetre'

    @classmethod
    def from_string(cls, name: str) -> Self:
        return next(attribute for attribute in cls if attribute.value == name)

    @classmethod
    def to_list(cls) -> list[str]:
        return list(attribute.value for attribute in cls)


def get_resource(filename: Path) -> str:
    """Retourne le contenu de la ressource situé au chemin donné"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


def get_help(mode: View) -> str:
    """Retourne le texte d'aide à afficher en fonction de la vue"""
    start_h1 = end_h1 = start_paragraph = end_paragraph = return_line = img = ""
    if mode == View.WINDOW:
        start_h1 = "<h1>"
        end_h1 = "</h1>"
        start_paragraph = "<p>"
        end_paragraph = "</p>"
        return_line = "<br />"
    preamble = PREAMBLE.format(start_h1=start_h1, end_h1=end_h1,
                               start_paragraph=start_paragraph, end_paragraph=end_paragraph,
                               return_line=return_line, SIZE_COMBINATION=SIZE_COMBINATION)
    return (f"{preamble}\n\nEntrez votre combinaison secrète en utilisant les chiffres des couleurs disponibles.\n"
            if mode == View.CONSOLE else
            f"{preamble}\n{get_resource(HTML_DIR / "help.html")}")
