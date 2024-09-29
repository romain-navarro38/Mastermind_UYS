from enum import Enum

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QLabel

from mastermind.utils.parameters import Color


class PieceSize(Enum):
    """Définitions des tailles pour les différents pions"""
    CLUE = 8
    COLOR = 40
    TRY = 32
    SECRET = 32


class Piece(QLabel):
    """Représentation d'un pion"""
    def __init__(self, color: Color = Color.BLACK, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.color = color


class PieceClue(Piece):
    """Représentation d'un indice."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setMaximumSize(PieceSize.CLUE.value, PieceSize.CLUE.value)
        self.setMinimumSize(PieceSize.CLUE.value, PieceSize.CLUE.value)
        self.radius = PieceSize.CLUE.value // 2
        self.set_color(Color.BLACK)

    def set_color(self, color: Color) -> None:
        """Associe une Color au pion et lui applique"""
        self.color = color
        self.setStyleSheet(f"border-radius: {self.radius}px;background-color: {color.value};")


class PieceColor(Piece):
    """Label cliquable retournant sa propre couleur."""
    clicked = Signal(Color)
    number = 0

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setMaximumSize(PieceSize.COLOR.value, PieceSize.COLOR.value)
        self.setMinimumSize(PieceSize.COLOR.value, PieceSize.COLOR.value)
        self.radius = PieceSize.COLOR.value // 2
        self.set_color(self.color)
        PieceColor.number += 1
        self.setText(f"{PieceColor.number}")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        """Emission du signal clicked, portant la couleur du pion cliqué"""
        self.clicked.emit(self.color)

    def set_color(self, color: Color) -> None:
        """Associe une Color au pion et lui applique"""
        self.color = color
        self.setStyleSheet(
            f"""border-radius: {self.radius}px;
            background-color: {color.value};
            font-size: 14px;
            font-weight: bold;
            color: {color.get_opposite()}""")


class PieceSecret(Piece):
    """Label qui compose la combinaison secrète."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setMaximumSize(PieceSize.SECRET.value, PieceSize.SECRET.value)
        self.setMinimumSize(PieceSize.SECRET.value, PieceSize.SECRET.value)
        self.radius = PieceSize.SECRET.value // 2
        self.set_color(Color.GRAY)
        self.setText("?")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_color(self, color: Color) -> None:
        """Applique une couleur au pion"""
        self.setStyleSheet(f"border-radius: {self.radius}px;background-color: {color.value};")


class PieceTry(Piece):
    """Représentation d'un pion de la couleur choisie
    par l'utilisateur. Devient le pion 'sélectionné' de la
    ligne qu'il compose lorsqu'il est cliqué."""
    clicked = Signal()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setMaximumSize(PieceSize.TRY.value, PieceSize.TRY.value)
        self.setMinimumSize(PieceSize.TRY.value, PieceSize.TRY.value)
        self.radius = PieceSize.TRY.value // 2
        self.is_selected = False
        self.next_piece = self.previous_piece = None

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        """Emission du signal clicked"""
        self.clicked.emit()

    def setEnabled(self, arg__1: bool) -> None:
        """Défini l'état d'activation (True ou False) du pion"""
        super().setEnabled(arg__1)
        if not arg__1:
            self.set_selected(arg__1)

    def set_color(self, color: Color) -> None:
        """Défini et applique une couleur au pion et ajoute une bordure
        s'il est à l'état 'sélectionné'."""
        self.color = color
        self.setStyleSheet(
            f"border-radius: {self.radius}px;"
            f"background-color: {color.value};"
            f"border-color: {'green red blue yellow' if self.is_selected else ''};"
            f"border-width: {'2px' if self.is_selected else '0px'};"
            "border-style: solid;"
        )

    def set_selected(self, selected: bool) -> None:
        """Change l'état 'sélectionné' à True ou False du pion
        et modifie son apparence."""
        self.is_selected = selected
        self.set_color(self.color)
