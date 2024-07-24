from enum import StrEnum, auto
from functools import partial

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QWidget, QSizePolicy, QFrame, QLabel, QSpacerItem

from mastermind.game.parameter import Color, SIZE_COMBINATION
from mastermind.window.piece import PieceClue, PieceTry, PieceSecret


class Status(StrEnum):
    ON_HOLD = auto()
    ACTIVATED = auto()
    DEACTIVATED = auto()


class VerticalSeparator(QFrame):
    def __init__(self, enabled: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_color(enabled)
        self.setFrameShape(QFrame.Shape.VLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)

    def set_color(self, enabled: bool):
        self.setStyleSheet(f"background-color: {Color.WHITE if enabled else Color.BLACK}")


class Row(QHBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = QLabel('')
        self.title.setStyleSheet("color: black;")
        self.title.setMinimumSize(QSize(20, 0))
        self.colors_layout = QHBoxLayout()
        self.clues_layout = QGridLayout()


# noinspection PyTypeChecker
class RowSecret(Row):
    """Représente la ligne contenant la combinaison secrète."""
    def __init__(self, secret_colours: list[Color], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title.setStyleSheet("color: white;")
        self.title.setText("?")
        self.addWidget(self.title)
        separator1 = VerticalSeparator(Color.WHITE)
        self.addWidget(separator1)
        for i in range(SIZE_COMBINATION):
            piece_secret = PieceSecret(secret_colours[i])
            self.colors_layout.addWidget(piece_secret)
        self.addLayout(self.colors_layout)
        separator2 = VerticalSeparator(Color.WHITE)
        self.addWidget(separator2)
        self.game_over = QLabel('')
        self.game_over.setStyleSheet("color: white;")
        sizepolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.game_over.setSizePolicy(sizepolicy)
        self.game_over.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.game_over)

    def reveal_combination(self, winner: bool):
        """Modifie l'apparence de la ligne pour révéler la combinaison
        secrète et afficher si la partie est gagnée ou perdue."""
        for i in range(self.colors_layout.count()):
            piece_secret: PieceSecret = self.colors_layout.itemAt(i).widget()
            piece_secret.set_color(piece_secret.color)
            piece_secret.setText('')
        self.game_over.setText("Gagné" if winner else "Perdu")


# noinspection PyUnresolvedReferences
class RowTry(Row):
    """Représente une ligne d'essai."""
    def __init__(self, window: QWidget, row_number: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title.setText(f"{row_number}")
        pieces_try = [PieceTry(Color.BLACK) for _ in range(SIZE_COMBINATION)]
        for i in range(SIZE_COMBINATION):
            piece_try = pieces_try[i]
            piece_try.next_piece = pieces_try[i + 1 if i < 3 else 0]
            piece_try.clicked.connect(partial(window.piece_selected, piece_try))
            self.colors_layout.addWidget(piece_try)
            piece_clue = PieceClue()
            self.clues_layout.addWidget(piece_clue, i // 2, i % 2, 1, 1)

        self.addWidget(self.title)
        self.separator1 = VerticalSeparator()
        self.addWidget(self.separator1)
        self.addLayout(self.colors_layout)
        self.separator2 = VerticalSeparator()
        self.addWidget(self.separator2)
        self.addLayout(self.clues_layout)
        verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.addSpacerItem(verticalSpacer)
        self.set_status(Status.ON_HOLD)

    def set_status(self, status: Status):
        """Modifie l'apparence de la ligne en fonction de l'état donné."""
        for i in range(self.colors_layout.count()):
            match status:
                case Status.ON_HOLD:
                    self.colors_layout.itemAt(i).widget().set_color(Color.BLACK)
                    self.colors_layout.itemAt(i).widget().setEnabled(False)
                case Status.ACTIVATED:
                    self.colors_layout.itemAt(i).widget().set_color(Color.GRAY)
                    self.title.setStyleSheet("color: white;")
                    self.separator1.set_color(True)
                    self.separator2.set_color(True)
                    self.colors_layout.itemAt(i).widget().setEnabled(True)
                case Status.DEACTIVATED:
                    self.colors_layout.itemAt(i).widget().setEnabled(False)

        if status == Status.ACTIVATED:
            self.colors_layout.itemAt(0).widget().set_selected(True)

    def select_next_try_piece(self):
        """Passe à l'état 'sélecionné' le pion qui suit celui
        qui est actuellement 'sélectionné' dans la ligne."""
        piece_try: PieceTry = next(
            (self.colors_layout.itemAt(i).widget() for i in range(self.colors_layout.count())
             if self.colors_layout.itemAt(i).widget().is_selected),
            None
        )
        piece_try.set_selected(False)
        piece_try.next_piece.set_selected(True)
