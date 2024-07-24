from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QPushButton, QSpacerItem, \
    QSizePolicy

from mastermind.game.game import Mastermind
from mastermind.game.parameter import Color, RESOURCE_DIR
from mastermind.window.piece import PieceColor, PieceTry
from mastermind.window.row import RowTry, Status, RowSecret


class MainWindow(QWidget):
    """Fenêtre principale"""
    def __init__(self, mastermind: Mastermind):
        super().__init__()

        self.mastermind = mastermind
        self.setWindowTitle("Combinaison secrète - Up Your Skills")
        self.setWindowIcon((QIcon(QPixmap(RESOURCE_DIR / "logo.ico"))))
        self.setup_ui()
        self.setStyleSheet("background-color: black;")

    def setup_ui(self):
        self.main_layout = QGridLayout(self)
        self.tries_layout = QVBoxLayout()
        self.color_layout = QVBoxLayout()
        self.color_layout.setContentsMargins(20, 0, 0, 0)

        self.rows = {}
        for i in range(self.mastermind.max_tries.value):
            row = RowTry(self, i + 1)
            self.rows[i] = row
            self.tries_layout.addLayout(row)
        self.rows[0].set_status(Status.ACTIVATED)
        self.row_actived = 0

        self.row_secret = RowSecret(self.mastermind.secret_combinaison)

        font_bold = QFont()
        font_bold.setBold(True)

        self.btn_rules = QPushButton("Règles du jeu")
        self.btn_rules.setFont(font_bold)
        self.btn_rules.setStyleSheet("background-color: gray")
        self.btn_rules.setMinimumSize(QSize(0, 30))
        self.btn_rules.clicked.connect(self.open_window_rules)
        self.color_layout.addWidget(self.btn_rules)

        verticalSpacer1 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.color_layout.addSpacerItem(verticalSpacer1)

        label_select_color = QLabel("Sélectionner vos couleurs")
        label_select_color.setStyleSheet("color: white;")
        label_select_color.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.color_layout.addWidget(label_select_color)

        select_colors_layout = QGridLayout()
        for i, (color, _) in enumerate(zip(Color, range(self.mastermind.level.value))):
            piece_color = PieceColor(color)
            piece_color.clicked.connect(self.positioned_color)
            select_colors_layout.addWidget(piece_color, i // 2, i % 2, 1, 1)
        self.color_layout.addLayout(select_colors_layout)

        verticalSpacer2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.color_layout.addSpacerItem(verticalSpacer2)

        self.btn_try = QPushButton("Proposer")
        self.btn_try.setFont(font_bold)
        self.btn_try.setStyleSheet("background-color: gray")
        self.btn_try.setMinimumSize(QSize(0, 30))
        self.btn_try.setEnabled(False)
        self.btn_try.clicked.connect(self.validate_combinaison)
        self.color_layout.addWidget(self.btn_try)

        verticalSpacer3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.color_layout.addSpacerItem(verticalSpacer3)

        self.main_layout.addLayout(self.tries_layout, 0, 0, 1, 1)
        self.main_layout.addLayout(self.color_layout, 0, 1, 1, 1)
        self.main_layout.addLayout(self.row_secret, 1, 0, 1, 2)

    def piece_selected(self, piece_try: PieceTry):
        """Le pion cliqué passe à l'état sélectionné. Les autres
        sont désectionnés s'ils l'étaient."""
        try_layout = self.rows[self.row_actived].children()[0]
        for i in range(try_layout.count()):
            try_layout.itemAt(i).widget().set_selected(False)
        piece_try.set_selected(True)

    def positioned_color(self, color: Color):
        """Une couleur est appliquée au pion à l'état sélectionné."""
        try_layout = self.rows[self.row_actived].colors_layout
        for i in range(try_layout.count()):
            if try_layout.itemAt(i).widget().is_selected:
                try_layout.itemAt(i).widget().set_color(color)
                break
        self.rows[self.row_actived].select_next_try_piece()
        self.btn_try.setEnabled(self.valided_row())

    def validate_combinaison(self):
        """Déclenche les actions suite à la validation d'une ligne :
            - Affichage des indices,
            - Désactivation de la ligne d'essai actuelle,
            - Désactive le bouton de proposition,
            - Vérification de l'état de la partie."""
        self.display_clues(self.mastermind.evaluate_combinaison(self.get_try_combination()))
        self.rows[self.row_actived].set_status(Status.DEACTIVATED)
        self.btn_try.setEnabled(False)
        self.is_game_over()

    def get_try_combination(self) -> list[Color]:
        """Récupère la liste des couleurs de la ligne active."""
        try_layout = self.rows[self.row_actived].colors_layout
        return [try_layout.itemAt(i).widget().color for i in range(try_layout.count())]

    def valided_row(self) -> bool:
        """Retourne True si une couleur a été appliquée à chaque pion."""
        return Color.GRAY not in self.get_try_combination()

    def display_clues(self, clues: list[Color]):
        """Affiche dans la ligne active les couleurs des indices
        passés en paramètres."""
        clue_layout = self.rows[self.row_actived].clues_layout
        for i, color in enumerate(clues):
            clue_layout.itemAt(i).widget().set_color(color)

    def is_game_over(self):
        """Si la partie est terminée, lance son affichage, sinon
        lance l'activation de la prochaine ligne d'essai."""
        if self.mastermind.game_over:
            self.display_game_over()
        else:
            self.activate_next_try()

    def activate_next_try(self):
        """Activation d'une nouvelle ligne d'essai"""
        self.row_actived += 1
        self.rows[self.row_actived].set_status(Status.ACTIVATED)

    def display_game_over(self):
        """Affichage de fin partie, la combinaison
        secrète est révélée."""
        self.row_secret.reveal_combination(self.mastermind.win)

    def open_window_rules(self):
        pass


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication()
    window = MainWindow(Mastermind())
    window.show()
    sys.exit(app.exec())
