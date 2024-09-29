from PySide6.QtCore import Qt, Signal, QEvent, QSize
from PySide6.QtGui import QIcon, QPixmap, QKeyEvent
from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QHBoxLayout, QComboBox

from mastermind.utils.parameters import Color, DIRECTORIES, Neighbor, Language, get_resource
from mastermind.views.confirmation import ConfirmationMessage
from mastermind.views.piece import PieceColor, PieceTry
from mastermind.views.row import RowTry, Status, RowSecret
from mastermind.views.custom_widget import Orientation, CustomSpacer, CustomButton


class MainWindow(QWidget):
    """Fenêtre principale"""
    evaluation_combination = Signal(list)
    event_keyboard = Signal(QKeyEvent)
    restart = Signal()
    show_rules = Signal()
    change_language = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        self.rows: dict[int, RowTry] = {}
        self.pieces_colors = []
        self.game_in_progress = False
        PieceColor.number = 0
        self.setWindowIcon((QIcon(QPixmap(DIRECTORIES['icon'] / "logo.png"))))
        self.setStyleSheet(get_resource(DIRECTORIES['style'] / "main.qss"))
        self.setMinimumWidth(450)

    def setup_ui(self, max_tries: int, level: int,
                 secret_combination: tuple[Color, ...],
                 language: Language,
                 translation: dict) -> None:
        """Chargement, modification, disposition et connexion des composants"""
        self._setup_ui_create_widgets(max_tries, level, secret_combination)
        self._setup_ui_modify_widgets(language)
        self._setup_ui_create_layouts()
        self._setup_ui_add_widgets_to_layouts()
        self._setup_ui_connections()
        self.setup_ui_translation(translation)
        self.setFocus()

    def _setup_ui_create_widgets(self, max_tries: int,
                       level: int,
                       secret_combination: tuple[Color, ...]) -> None:
        for i in range(max_tries):
            row = RowTry(self, i + 1)
            self.rows[i] = row

        self.row_secret = RowSecret(secret_combination)

        self.horizontal_spacer = CustomSpacer(Orientation.HORIZONTAL)
        self.cb_language = QComboBox()
        self.vertical_spacer_1 = CustomSpacer(Orientation.VERTICAL)
        self.lab_select_color = QLabel()

        for color, _ in zip(Color, range(level)):
            piece_color = PieceColor(color)
            self.pieces_colors.append(piece_color)

        self.vertical_spacer_2 = CustomSpacer(Orientation.VERTICAL)
        self.btn_try = CustomButton()
        self.vertical_spacer_3 = CustomSpacer(Orientation.VERTICAL)

        self.btn_help = CustomButton()
        self.btn_new_game = CustomButton()
        self.btn_quit = CustomButton()

    def _setup_ui_modify_widgets(self, language: Language) -> None:
        self.rows[0].set_status(Status.ACTIVATED)
        self.num_row_enabled = 0

        for lang in Language:
            self.cb_language.addItem(lang.name, lang)
        self.cb_language.setCurrentIndex(self.cb_language.findData(language))
        self.cb_language.setFixedSize(QSize(60, 30))

        self.lab_select_color.setStyleSheet("color: white;")
        self.lab_select_color.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_try.setEnabled(False)
        self.btn_try.setObjectName("btn_try")

    def _setup_ui_create_layouts(self) -> None:
        self.main_layout = QGridLayout(self)
        self.tries_layout = QVBoxLayout()
        self.translate_layout = QHBoxLayout()
        self.color_layout = QVBoxLayout()
        self.color_layout.setContentsMargins(20, 0, 0, 0)
        self.select_colors_layout = QGridLayout()
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setContentsMargins(0, 20, 0, 0)

    def _setup_ui_add_widgets_to_layouts(self) -> None:
        for row in self.rows.values():
            self.tries_layout.addLayout(row)

        self.translate_layout.addSpacerItem(self.horizontal_spacer)
        self.translate_layout.addWidget(self.cb_language)
        self.color_layout.addLayout(self.translate_layout)
        self.color_layout.addSpacerItem(self.vertical_spacer_1)
        self.color_layout.addWidget(self.lab_select_color)
        self.color_layout.addLayout(self.select_colors_layout)

        for i, piece_color in enumerate(self.pieces_colors):
            self.select_colors_layout.addWidget(piece_color, i // 2, i % 2, 1, 1)

        self.color_layout.addSpacerItem(self.vertical_spacer_2)
        self.color_layout.addWidget(self.btn_try)
        self.color_layout.addSpacerItem(self.vertical_spacer_3)

        self.buttons_layout.addWidget(self.btn_help)
        self.buttons_layout.addWidget(self.btn_new_game)
        self.buttons_layout.addWidget(self.btn_quit)

        self.main_layout.addLayout(self.tries_layout, 0, 0, 1, 1)
        self.main_layout.addLayout(self.color_layout, 0, 1, 1, 1)
        self.main_layout.addLayout(self.row_secret, 1, 0, 1, 2)
        self.main_layout.addLayout(self.buttons_layout, 2, 0, 1, 2)

    def _setup_ui_connections(self) -> None:
        self.cb_language.currentIndexChanged.connect(self._emit_change_language)

        for piece_color in self.pieces_colors:
            piece_color.clicked.connect(self.positioned_color)

        self.btn_try.clicked.connect(self.validate_combinaison)

        self.btn_help.clicked.connect(self.show_rules.emit)
        self.btn_new_game.clicked.connect(self.restart.emit)
        self.btn_quit.clicked.connect(self.close)

    def setup_ui_translation(self, translation: dict) -> None:
        self.translation = translation
        self.setWindowTitle(translation['main_title'])
        self.lab_select_color.setText(translation['select_color'])
        self.btn_try.setText(translation['submit_button'])
        self.btn_quit.setText(translation['quit_button'])
        self.btn_help.setText(translation['help_button'])
        self.btn_new_game.setText(translation['new_game'])

    def _emit_change_language(self) -> None:
        self.change_language.emit(self.cb_language.currentData())
        self.setFocus()

    def _is_active_row_valid(self) -> bool:
        """Retourne True si une couleur a été appliquée à chaque pion."""
        return Color.GRAY not in self._get_try_combination()

    def _get_try_combination(self) -> list[Color]:
        """Récupère la liste des couleurs de la ligne active."""
        try_layout = self.rows[self.num_row_enabled].colors_layout
        return [try_layout.itemAt(i).widget().color for i in range(try_layout.count())]

    def activate_next_try(self) -> None:
        """Activation de la prochaine ligne d'essai"""
        self.num_row_enabled += 1
        self.rows[self.num_row_enabled].set_status(Status.ACTIVATED)

    def closeEvent(self, event: QEvent) -> None:
        """Gère les événements de fermeture.
        Demande confirmation si une partie est en cours"""
        if self.game_in_progress:
            event.accept() if self.confirmation_interruption() else event.ignore()

    def confirmation_interruption(self) -> bool:
        """Retourne le choix de l'utilisateur via une boite de dialogue
        d'interrompre la partie en cours"""
        dialog = ConfirmationMessage(self)
        if dialog.exec():
            return True
        self.setFocus()
        return False

    def deactivate_row(self) -> None:
        """Désactivation de la ligne active"""
        self.rows[self.num_row_enabled].set_status(Status.DEACTIVATED)
        self.btn_try.setEnabled(False)

    def display_clues(self, clues: tuple[Color]) -> None:
        """Affiche dans la ligne active les couleurs des indices
        passés en paramètres."""
        clue_layout = self.rows[self.num_row_enabled].clues_layout
        for i, color in enumerate(clues):
            clue_layout.itemAt(i).widget().set_color(color)

    def display_game_over(self, is_win: bool) -> None:
        """Affichage de fin partie, la combinaison
        secrète est révélée."""
        self.row_secret.reveal_combination(is_win, self.translation)

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
        self.btn_try.setEnabled(self._is_active_row_valid())

    def validate_combinaison(self) -> None:
        """Émet dans un signal la combinaison de la ligne active"""
        self.evaluation_combination.emit(self._get_try_combination())
        self.setFocus()
