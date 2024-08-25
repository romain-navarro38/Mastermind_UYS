from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QPushButton, QSpacerItem, \
    QSizePolicy

from mastermind.model.parameters import Color, RESOURCE_DIR
from mastermind.views.piece import PieceColor, PieceTry
from mastermind.views.row import RowTry, Status, RowSecret


class MainWindow(QWidget):
    """Fenêtre principale"""

    evaluation_combination = Signal(list)

    def __init__(self) -> None:
        super().__init__()
        self.rows = {}
        self.pieces_colors = []

    def setup_ui(self, max_tries: int, level: int, secret_combination: list[Color]) -> None:
        self.setWindowTitle("Combinaison secrète - Up Your Skills")
        print(RESOURCE_DIR)
        self.setWindowIcon((QIcon(QPixmap(RESOURCE_DIR / "logo.ico"))))
        self.setStyleSheet("background-color: black;")
        self.create_widgets(max_tries, level, secret_combination)
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self, max_tries: int, level: int, secret_combination: list[Color]):
        for i in range(max_tries):
            row = RowTry(self, i + 1)
            self.rows[i] = row

        self.btn_rules = QPushButton("Règles du jeu")

        self.row_secret = RowSecret(secret_combination)

        self.vertical_spacer_1 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.lab_select_color = QLabel("Sélectionner vos couleurs")

        for color, _ in zip(Color, range(level)):
            piece_color = PieceColor(color)
            self.pieces_colors.append(piece_color)

        self.vertical_spacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.btn_try = QPushButton("Proposer")

        self.vertical_spacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

    def modify_widgets(self):
        self.rows[0].set_status(Status.ACTIVATED)
        self.row_actived = 0

        font_bold = QFont()
        font_bold.setBold(True)

        self.btn_rules.setFont(font_bold)
        self.btn_rules.setStyleSheet("background-color: gray")
        self.btn_rules.setMinimumSize(QSize(0, 30))

        self.lab_select_color.setStyleSheet("color: white;")
        self.lab_select_color.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_try.setFont(font_bold)
        self.btn_try.setStyleSheet("background-color: gray")
        self.btn_try.setMinimumSize(QSize(0, 30))
        self.btn_try.setEnabled(False)

    def create_layouts(self):
        self.main_layout = QGridLayout(self)
        self.tries_layout = QVBoxLayout()
        self.color_layout = QVBoxLayout()
        self.color_layout.setContentsMargins(20, 0, 0, 0)
        self.select_colors_layout = QGridLayout()

    def add_widgets_to_layouts(self):
        for row in self.rows.values():
            self.tries_layout.addLayout(row)

        self.color_layout.addWidget(self.btn_rules)
        self.color_layout.addSpacerItem(self.vertical_spacer_1)
        self.color_layout.addWidget(self.lab_select_color)
        self.color_layout.addLayout(self.select_colors_layout)

        for i, piece_color in enumerate(self.pieces_colors):
            self.select_colors_layout.addWidget(piece_color, i // 2, i % 2, 1, 1)

        self.color_layout.addSpacerItem(self.vertical_spacer_2)
        self.color_layout.addWidget(self.btn_try)
        self.color_layout.addSpacerItem(self.vertical_spacer_3)

        self.main_layout.addLayout(self.tries_layout, 0, 0, 1, 1)
        self.main_layout.addLayout(self.color_layout, 0, 1, 1, 1)
        self.main_layout.addLayout(self.row_secret, 1, 0, 1, 2)

    def setup_connections(self):
        self.btn_rules.clicked.connect(self.open_window_rules)

        for piece_color in self.pieces_colors:
            piece_color.clicked.connect(self.positioned_color)

        self.btn_try.clicked.connect(self.validate_combinaison)

    def piece_selected(self, piece_try: PieceTry) -> None:
        """Le pion cliqué passe à l'état sélectionné. Les autres
        sont désélectionnés s'ils l'étaient."""
        try_layout = self.rows[self.row_actived].children()[0]
        for i in range(try_layout.count()):
            try_layout.itemAt(i).widget().set_selected(False)
        piece_try.set_selected(True)

    def positioned_color(self, color: Color) -> None:
        """Une couleur est appliquée au pion à l'état sélectionné."""
        try_layout = self.rows[self.row_actived].colors_layout
        for i in range(try_layout.count()):
            if try_layout.itemAt(i).widget().is_selected:
                try_layout.itemAt(i).widget().set_color(color)
                break
        self.rows[self.row_actived].select_next_try_piece()
        self.btn_try.setEnabled(self.valided_row())

    def validate_combinaison(self) -> None:
        """Déclenche les actions suite à la validation d'une ligne :
            - Affichage des indices,
            - Désactivation de la ligne d'essai actuelle,
            - Désactive le bouton de proposition,
            - Vérification de l'état de la partie."""
        self.evaluation_combination.emit(self.get_try_combination())

    def deactivate_row(self):
        self.rows[self.row_actived].set_status(Status.DEACTIVATED)
        self.btn_try.setEnabled(False)

    def get_try_combination(self) -> list[Color]:
        """Récupère la liste des couleurs de la ligne active."""
        try_layout = self.rows[self.row_actived].colors_layout
        return [try_layout.itemAt(i).widget().color for i in range(try_layout.count())]

    def valided_row(self) -> bool:
        """Retourne True si une couleur a été appliquée à chaque pion."""
        return Color.GRIS not in self.get_try_combination()

    def display_clues(self, clues: list[Color]) -> None:
        """Affiche dans la ligne active les couleurs des indices
        passés en paramètres."""
        clue_layout = self.rows[self.row_actived].clues_layout
        for i, color in enumerate(clues):
            clue_layout.itemAt(i).widget().set_color(color)

    def is_game_over(self) -> None:
        """Si la partie est terminée, lance son affichage, sinon
        lance l'activation de la prochaine ligne d'essai."""
        if self.mastermind.game_over:
            self.display_game_over()
        else:
            self.activate_next_try()

    def activate_next_try(self) -> None:
        """Activation d'une nouvelle ligne d'essai"""
        self.row_actived += 1
        self.rows[self.row_actived].set_status(Status.ACTIVATED)

    def display_game_over(self, is_win: bool) -> None:
        """Affichage de fin partie, la combinaison
        secrète est révélée."""
        self.row_secret.reveal_combination(is_win)

    def open_window_rules(self) -> None:
        pass
