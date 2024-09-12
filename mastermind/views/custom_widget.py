from enum import Enum, auto

from PySide6.QtCore import QSize
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QSpacerItem, QSizePolicy, QPushButton

from mastermind.utils.parameters import get_resource, DIRECTORIES

font_bold = QFont()
font_bold.setBold(True)


class Orientation(Enum):
    """Défini des constantes pour l'orientation"""
    VERTICAL = auto()
    HORIZONTAL = auto()


class CustomButton(QPushButton):
    """QPushButton personnalisé"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setFont(font_bold)
        self.setStyleSheet(get_resource(DIRECTORIES['style'] / "custom_button.qss"))
        self.setMinimumSize(QSize(0, 30))


class CustomSpacer(QSpacerItem):
    """Défini un QSpacerItem en fonction de l'orientation voulue"""
    def __init__(self, orientation: Orientation) -> None:
        if orientation == Orientation.VERTICAL:
            super().__init__(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        else:
            super().__init__(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
