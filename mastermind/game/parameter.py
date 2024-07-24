from enum import Enum, StrEnum
from pathlib import Path

RESOURCE_DIR = Path().cwd().parent.parent / "resource"
SIZE_COMBINATION = 4

class Color(StrEnum):
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


class Level(Enum):
    EASY = 4
    NORMAL = 6
    DIFFICULT = 8


class Try(Enum):
    EASY = 12
    NORMAL = 10
