from enum import Enum, auto

from PySide6.QtWidgets import QSpacerItem, QSizePolicy


class Orientation(Enum):
    """Défini des constantes pour l'orientation"""
    VERTICAL = auto()
    HORIZONTAL = auto()


class CustomSpacer(QSpacerItem):
    """Défini un QSpacerItem en fonction de l'orientation voulue"""
    def __init__(self, orientation: Orientation):
        if orientation == Orientation.VERTICAL:
            super().__init__(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        else:
            super().__init__(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
