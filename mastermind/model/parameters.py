from enum import Enum, StrEnum
from pathlib import Path
from typing import Self

RESOURCE_DIR = Path(__file__).parent.parent.parent / "resource"
SIZE_COMBINATION = 4
SQUARE = "\u25A0"  # correspondant à ■
DOT = "\u25CF"  # correspondant à ●
RESET_COLOR = "\033[0m"
PREAMBLE = f"""JEU DU MASTERMIND
Trouver la bonne combinaison de {SIZE_COMBINATION} couleurs secrètes que notre 'IA' aura généré.
A chaque couleur bien positionnée, vous aurez en retour un indicateur rouge.
A chaque couleur présente mais mal positionnée, vous aurez en retour un indicateur blanc.

Entrez votre combinaison secrète en utilisant les chiffres des couleurs disponibles.
"""


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


if __name__ == '__main__':
    for color in Color:
        rouge, vert, bleu = color.to_rgb()
        print(f"{color.name.capitalize()} : {rouge=}, {vert=}, {bleu=}")
