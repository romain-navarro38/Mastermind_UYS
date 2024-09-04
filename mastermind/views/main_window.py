from PySide6.QtCore import Qt, QSize, Signal, QEvent
from PySide6.QtGui import QIcon, QPixmap, QFont, QKeyEvent
from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QPushButton, QHBoxLayout

from mastermind.utils.parameters import Color, RESOURCE_DIR, Neighbor, Level, Try
from mastermind.views.confirmation import ConfirmationMessage
from mastermind.views.new_game import NewGame
from mastermind.views.piece import PieceColor, PieceTry
from mastermind.views.row import RowTry, Status, RowSecret
from mastermind.views.spacer import Orientation, CustomSpacer


class MainWindow(QWidget):
    """Fenêtre principale"""
    evaluation_combination = Signal(list)
    event_keyboard = Signal(QKeyEvent)
    restart = Signal(Level, Try)

    def __init__(self) -> None:
        super().__init__()
        self.rows: dict[int, RowTry] = {}
        self.pieces_colors = []
        self.game_in_progress = False

    def setup_ui(self, max_tries: int, level: int, secret_combination: list[Color]) -> None:
        """Chargement, modification, disposition et connexion des composants"""
        self.setWindowTitle("Devine la combinaison secrète - Up Your Skills")
        self.setWindowIcon((QIcon(QPixmap(RESOURCE_DIR / "logo.ico"))))
        self.setStyleSheet("background-color: black;")
        self.create_widgets(max_tries, level, secret_combination)
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()
        self.setFocus()

    def create_widgets(self, max_tries: int, level: int, secret_combination: list[Color]):
        for i in range(max_tries):
            row = RowTry(self, i + 1)
            self.rows[i] = row

        self.row_secret = RowSecret(secret_combination)
        self.vertical_spacer_1 = CustomSpacer(Orientation.VERTICAL)
        self.lab_select_color = QLabel("Sélectionner vos couleurs")

        for color, _ in zip(Color, range(level)):
            piece_color = PieceColor(color)
            self.pieces_colors.append(piece_color)

        self.vertical_spacer_2 = CustomSpacer(Orientation.VERTICAL)
        self.btn_try = QPushButton("Proposer")
        self.vertical_spacer_3 = CustomSpacer(Orientation.VERTICAL)

        self.btn_rules = QPushButton("Règles du jeu")
        self.btn_new_game = QPushButton("Nouvelle partie")
        self.btn_quit = QPushButton("Quitter")

    def modify_widgets(self):
        self.rows[0].set_status(Status.ACTIVATED)
        self.num_row_enabled = 0

        font_bold = QFont()
        font_bold.setBold(True)

        self.lab_select_color.setStyleSheet("color: white;")
        self.lab_select_color.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_try.setFont(font_bold)
        self.btn_try.setStyleSheet("background-color: gray")
        self.btn_try.setMinimumSize(QSize(0, 30))
        self.btn_try.setEnabled(False)

        self.btn_rules.setFont(font_bold)
        self.btn_rules.setStyleSheet("background-color: gray")
        self.btn_rules.setMinimumSize(QSize(0, 30))

        self.btn_new_game.setFont(font_bold)
        self.btn_new_game.setStyleSheet("background-color: gray")
        self.btn_new_game.setMinimumSize(QSize(0, 30))

        self.btn_quit.setFont(font_bold)
        self.btn_quit.setStyleSheet("background-color: gray")
        self.btn_quit.setMinimumSize(QSize(0, 30))

    def create_layouts(self):
        self.main_layout = QGridLayout(self)
        self.tries_layout = QVBoxLayout()
        self.color_layout = QVBoxLayout()
        self.color_layout.setContentsMargins(20, 0, 0, 0)
        self.select_colors_layout = QGridLayout()
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setContentsMargins(0, 20, 0, 0)

    def add_widgets_to_layouts(self):
        for row in self.rows.values():
            self.tries_layout.addLayout(row)

        self.color_layout.addSpacerItem(self.vertical_spacer_1)
        self.color_layout.addWidget(self.lab_select_color)
        self.color_layout.addLayout(self.select_colors_layout)

        for i, piece_color in enumerate(self.pieces_colors):
            self.select_colors_layout.addWidget(piece_color, i // 2, i % 2, 1, 1)

        self.color_layout.addSpacerItem(self.vertical_spacer_2)
        self.color_layout.addWidget(self.btn_try)
        self.color_layout.addSpacerItem(self.vertical_spacer_3)

        self.buttons_layout.addWidget(self.btn_rules)
        self.buttons_layout.addWidget(self.btn_new_game)
        self.buttons_layout.addWidget(self.btn_quit)

        self.main_layout.addLayout(self.tries_layout, 0, 0, 1, 1)
        self.main_layout.addLayout(self.color_layout, 0, 1, 1, 1)
        self.main_layout.addLayout(self.row_secret, 1, 0, 1, 2)
        self.main_layout.addLayout(self.buttons_layout, 2, 0, 1, 2)

    def setup_connections(self):
        for piece_color in self.pieces_colors:
            piece_color.clicked.connect(self.positioned_color)

        self.btn_try.clicked.connect(self.validate_combinaison)

        self.btn_rules.clicked.connect(self.open_window_rules)
        self.btn_new_game.clicked.connect(self.new_game)
        self.btn_quit.clicked.connect(self.close)

    def confirmation_interruption(self) -> bool:
        """Retourne le choix de l'utilisateur via une boite de dialogue
        d'interrompre la partie en cours"""
        dialog = ConfirmationMessage(self)
        if dialog.exec():
            return True
        self.setFocus()
        return False

    def closeEvent(self, event: QEvent) -> None:
        """Gère les événements de fermeture.
        Demande confirmation si une partie est en cours"""
        if self.game_in_progress:
            event.accept() if self.confirmation_interruption() else event.ignore()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Émet le signal event_keyboard avec la ou les touches
        tapées par l'utilisateur"""
        self.event_keyboard.emit(event)

    def piece_selected(self, piece_try: PieceTry) -> None:
        """Le pion cliqué passe à l'état sélectionné. Les autres
        sont désélectionnés s'ils l'étaient."""
        try_layout = self.rows[self.num_row_enabled].children()[0]
        for i in range(try_layout.count()):
            try_layout.itemAt(i).widget().set_selected(False)
        piece_try.set_selected(True)

    def positioned_color(self, color: Color) -> None:
        """Une couleur est appliquée au pion à l'état sélectionné."""
        try_layout = self.rows[self.num_row_enabled].colors_layout
        for i in range(try_layout.count()):
            if try_layout.itemAt(i).widget().is_selected:
                try_layout.itemAt(i).widget().set_color(color)
                break
        self.rows[self.num_row_enabled].select_neighbor_try_piece(Neighbor.RIGHT)
        self.btn_try.setEnabled(self.is_active_row_valid())

    def validate_combinaison(self) -> None:
        """Émet dans un signal la combinaison de la ligne active"""
        self.evaluation_combination.emit(self.get_try_combination())
        self.setFocus()

    def deactivate_row(self):
        """Désactivation de la ligne active"""
        self.rows[self.num_row_enabled].set_status(Status.DEACTIVATED)
        self.btn_try.setEnabled(False)

    def get_try_combination(self) -> list[Color]:
        """Récupère la liste des couleurs de la ligne active."""
        try_layout = self.rows[self.num_row_enabled].colors_layout
        return [try_layout.itemAt(i).widget().color for i in range(try_layout.count())]

    def is_active_row_valid(self) -> bool:
        """Retourne True si une couleur a été appliquée à chaque pion."""
        return Color.GRIS not in self.get_try_combination()

    def display_clues(self, clues: list[Color]) -> None:
        """Affiche dans la ligne active les couleurs des indices
        passés en paramètres."""
        clue_layout = self.rows[self.num_row_enabled].clues_layout
        for i, color in enumerate(clues):
            clue_layout.itemAt(i).widget().set_color(color)

    def activate_next_try(self) -> None:
        """Activation de la prochaine ligne d'essai"""
        self.num_row_enabled += 1
        self.rows[self.num_row_enabled].set_status(Status.ACTIVATED)

    def display_game_over(self, is_win: bool) -> None:
        """Affichage de fin partie, la combinaison
        secrète est révélée."""
        self.row_secret.reveal_combination(is_win)

    def new_game(self) -> None:
        if self.game_in_progress and not self.confirmation_interruption():
            return
        dialog = NewGame(self)
        if dialog.exec():
            self.restart.emit(*dialog.get_params_new_game())
        self.setFocus()

    def open_window_rules(self) -> None:
        self.setFocus()
