from enum import Enum, auto
from functools import partial

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QWidget, QSizePolicy, QFrame, QLabel

from mastermind.utils.parameters import Color, SIZE_COMBINATION, Neighbor
from mastermind.views.piece import PieceClue, PieceTry, PieceSecret
from mastermind.views.custom_widget import CustomSpacer, Orientation, font_bold


class Status(Enum):
    """Classe Enum représentant l'état d'une ligne d'essai"""
    ON_HOLD = auto()
    ACTIVATED = auto()
    DEACTIVATED = auto()


class VerticalSeparator(QFrame):
    """Ligne verticale servant de séparation entre les éléments de l'UI"""
    def __init__(self, enabled: bool = False) -> None:
        super().__init__()

        self.set_color(enabled)
        self.setFrameShape(QFrame.Shape.VLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)

    def set_color(self, enabled: bool) -> None:
        """Modifie la couleur en fonction de l'état d'activation voulu.
        Activé : blanc
        Désactivé : noir"""
        self.setStyleSheet(f"background-color: {Color.BLANC if enabled else Color.NOIR}")


class Row(QHBoxLayout):
    """Ligne verticale pour accueillir des pions (Piece)"""
    def __init__(self) -> None:
        super().__init__()

        self.la_title = QLabel('')
        self.la_title.setStyleSheet("color: black")
        self.la_title.setMinimumSize(QSize(20, 0))
        self.colors_layout = QHBoxLayout()
        self.clues_layout = QGridLayout()


class RowSecret(Row):
    """Représente la ligne contenant la combinaison secrète."""
    def __init__(self, secret_colours: list[Color]) -> None:
        super().__init__()

        self.la_title.setStyleSheet("color: white;")
        self.la_title.setText("?")
        self.addWidget(self.la_title)
        separator1 = VerticalSeparator(True)
        self.addWidget(separator1)
        for i in range(SIZE_COMBINATION):
            piece_secret = PieceSecret(secret_colours[i])
            self.colors_layout.addWidget(piece_secret)
        self.addLayout(self.colors_layout)
        separator2 = VerticalSeparator(True)
        self.addWidget(separator2)
        self.la_game_over = QLabel('')
        self.la_game_over.setStyleSheet("color: white;font-size: 16px;")
        self.la_game_over.setFont(font_bold)
        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.la_game_over.setSizePolicy(size_policy)
        self.la_game_over.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.la_game_over)

    def reveal_combination(self, winner: bool) -> None:
        """Modifie l'apparence de la ligne pour révéler la combinaison
        secrète et afficher si la partie est gagnée ou perdue."""
        for i in range(self.colors_layout.count()):
            piece_secret: PieceSecret = self.colors_layout.itemAt(i).widget()
            piece_secret.set_color(piece_secret.color)
            piece_secret.setText('')
        self.la_game_over.setText("Gagné !" if winner else "Perdu !")


class RowTry(Row):
    """Représente une ligne d'essai."""
    def __init__(self, parent: QWidget, row_number: int) -> None:
        super().__init__()

        self.la_title.setText(f"{row_number}")
        pieces_try = [PieceTry(Color.NOIR) for _ in range(SIZE_COMBINATION)]
        for i in range(SIZE_COMBINATION):
            piece_try = pieces_try[i]
            piece_try.next_piece = pieces_try[i + 1 if i < SIZE_COMBINATION - 1 else 0]
            piece_try.previous_piece = pieces_try[i - 1 if i > 0 else SIZE_COMBINATION - 1]
            piece_try.clicked.connect(partial(parent.piece_selected, piece_try))
            self.colors_layout.addWidget(piece_try)
            piece_clue = PieceClue()
            self.clues_layout.addWidget(piece_clue, i % 2, i // 2, 1, 1)

        self.addWidget(self.la_title)
        self.separator1 = VerticalSeparator()
        self.addWidget(self.separator1)
        self.addLayout(self.colors_layout)
        self.separator2 = VerticalSeparator()
        self.addWidget(self.separator2)
        self.addLayout(self.clues_layout)
        self.addSpacerItem(CustomSpacer(Orientation.HORIZONTAL))
        self.set_status(Status.ON_HOLD)

    def set_status(self, status: Status) -> None:
        """Modifie l'apparence de la ligne en fonction de l'état donné."""
        for i in range(self.colors_layout.count()):
            match status:
                case Status.ON_HOLD:
                    self.colors_layout.itemAt(i).widget().set_color(Color.NOIR)
                    self.colors_layout.itemAt(i).widget().setEnabled(False)
                case Status.ACTIVATED:
                    self.colors_layout.itemAt(i).widget().set_color(Color.GRIS)
                    self.la_title.setStyleSheet("color: white;")
                    self.separator1.set_color(True)
                    self.separator2.set_color(True)
                    self.colors_layout.itemAt(i).widget().setEnabled(True)
                case Status.DEACTIVATED:
                    self.colors_layout.itemAt(i).widget().setEnabled(False)

        if status == Status.ACTIVATED:
            self.colors_layout.itemAt(0).widget().set_selected(True)

    def select_neighbor_try_piece(self, neighbor: Neighbor) -> None:
        """Passe à l'état 'sélectionné' le pion qui suit ou précède celui
        qui est actuellement 'sélectionné' dans la ligne."""
        direction = (range(self.colors_layout.count())
                     if neighbor == Neighbor.RIGHT
                     else range(self.colors_layout.count() - 1, -1, -1))
        piece_try: PieceTry | None = next(
            (self.colors_layout.itemAt(i).widget() for i in direction
             if self.colors_layout.itemAt(i).widget().is_selected),
            None
        )
        if piece_try:
            piece_try.set_selected(False)
            (piece_try.next_piece.set_selected(True)
             if neighbor == Neighbor.RIGHT
             else piece_try.previous_piece.set_selected(True))
