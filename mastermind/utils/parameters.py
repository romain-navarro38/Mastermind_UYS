from enum import Enum, StrEnum, auto
from typing import Self


class Color(StrEnum):
    """Classe StrEnum représentant une couleur
    associé à son code hexadécimal"""
    YELLOW = '#ffff00'
    BLUE = '#0000ff'
    RED = '#ff0000'
    GREEN = '#00ff00'
    WHITE = '#ffffff'
    MAGENTA = '#ff00ff'
    CYAN = '#00ffff'
    BROWN = '#906434'
    BLACK = "#000000"
    GRAY = '#7f7f7f'

    @classmethod
    def from_index(cls, index: int) -> Self:
        """Retourne l'instance correspondant à l'index donné"""
        return list(cls)[index]

    def get_opposite(self) -> str:
        """Retourne la couleur opposée au format hexadécimal"""
        return f"#{''.join([f'{hex(255 - c)[2:]:02}' for c in self.to_rgb()])}"

    def to_rgb(self) -> tuple[int, ...]:
        """Retourne la couleur au format RGB"""
        return tuple(int(self.value[i:i + 2], 16) for i in range(1, len(self.value), 2))


class Language(StrEnum):
    FR = 'FR'
    EN = 'EN'

    @classmethod
    def to_list(cls) -> list[str]:
        return list(attribute.value for attribute in cls)

    @classmethod
    def from_string(cls, name: str) -> Self:
        """Retourne l'instance correspondant au nom donné"""
        return next(attribute for attribute in cls if attribute.name == name)


class Level(Enum):
    """Classe Enum représentant le nombre de couleurs disponible
    pour composer une combinaison"""
    EASY = 4
    NORMAL = 6
    HARD = 8

    def __str__(self):
        return self.name.lower()

    @classmethod
    def from_string(cls, name: str) -> Self:
        """Retourne l'instance correspondant au nom donné"""
        return next(attribute for attribute in cls if attribute.name.lower() == name.lower())

    @classmethod
    def to_list(cls) -> list[str]:
        """Retourne la liste de tous les attributs au format str"""
        return list(str(attribute) for attribute in cls)


class Neighbor(Enum):
    """Classe Enum représentant le pion voisin,
    à droite ou à gauche, dans une ligne d'essai"""
    RIGHT = auto()
    LEFT = auto()


class Try(Enum):
    """Classe Enum représentant le nombre maximum d'essais
    pour trouver la combinaison secrète"""
    EASY = 12
    NORMAL = 10

    def __str__(self):
        return self.name.lower()

    @classmethod
    def from_string(cls, name: str) -> Self:
        """Retourne l'instance correspondant au nom donné"""
        return next(attribute for attribute in cls if attribute.name.lower() == name)

    @classmethod
    def to_list(cls) -> list[str]:
        """Retourne la liste de tous les attributs au format str"""
        return list(str(attribute) for attribute in cls)


class View(StrEnum):
    """Classe StrEnum représentant une vue"""
    CONSOLE = 'console'
    WINDOW = 'window'

    @classmethod
    def from_string(cls, name: str) -> Self:
        """Retourne l'instance correspondant au nom donné"""
        return next(attribute for attribute in cls if attribute.value == name)

    @classmethod
    def to_list(cls) -> list[str]:
        """Retourne la liste de tous les attributs au format str"""
        return list(attribute.value for attribute in cls)
