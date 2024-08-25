from enum import Enum, StrEnum
from pathlib import Path

RESOURCE_DIR = Path(__file__).parent.parent.parent / "resource"
SIZE_COMBINATION = 4
SQUARE = "\u25A0"  # corresponding to ■
DOT = "\u25CF"  # corresponding to ●
RESET_COLOR = "\033[0m"
PREAMBLE = f"""JEU DU MASTERMIND
Trouver la bonne combinaison de {SIZE_COMBINATION} couleurs secrètes que notre 'IA' aura généré.
A chaque couleur bien positionnée, vous aurez en retour un indicateur rouge.
A chaque couleur présente mais mal positionnée, vous aurez en retour un indicateur blanc.

Entrez votre combinaison secrète en utilisant les chiffres des couleurs disponibles.
"""


class Color(StrEnum):
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


class Level(Enum):
    FACILE = 4
    NORMAL = 6
    DIFFICILE = 8


class Try(Enum):
    FACILE = 12
    NORMAL = 10


if __name__ == '__main__':
    print(RESOURCE_DIR)
