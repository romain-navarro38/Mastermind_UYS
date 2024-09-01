from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

from mastermind.model.game import Mastermind
from mastermind.utils.parameters import Color, Neighbor
from mastermind.views.main_window import MainWindow


class WindowController:
    def __init__(self, model: Mastermind, view: MainWindow) -> None:
        self.model = model
        self.view = view
        self.view.evaluation_combination.connect(self.evaluate_combination)
        self.view.event_keyboard.connect(self.parse_input)

    def load_ui(self) -> None:
        """Chargement des composants de la fenêtre"""
        self.view.setup_ui(self.model.max_tries.value, self.model.level.value, self.model.get_secret_combination())

    def is_game_over(self) -> bool:
        """Retourne True si la partie est terminée"""
        return self.model.game_over

    def is_win(self) -> bool:
        """Retourne True si la partie est gagnée"""
        return self.model.win

    def evaluate_combination(self, combination: list[Color]) -> None:
        """Obtient du modèle les indices associés à la combinaison évaluée
        et met à jour la vue en conséquence"""
        if (clues := self.model.evaluate_combinaison(combination)) is None:
            return
        self.view.display_clues(clues)
        self.view.deactivate_row()
        if self.is_game_over():
            self.view.game_in_progress = False
            self.view.display_game_over(self.is_win())
        else:
            self.view.game_in_progress = True
            self.view.activate_next_try()

    def run(self) -> None:
        """Affiche la fenêtre principale"""
        self.load_ui()
        self.view.show()

    def parse_input(self, event: QKeyEvent) -> None:
        """Déclenche, sur la vue, l'action associée à l'entrée clavier"""
        if event.modifiers() == Qt.ControlModifier:
            match event.key():
                case Qt.Key_Q:
                    self.view.close()
                case Qt.Key_N:
                    pass
                case Qt.Key_R:
                    self.view.open_window_rules()
        elif not self.is_game_over():
            match event.key():
                case num if 49 <= num <= 48 + self.model.level.value:
                    self.view.positioned_color(Color.from_index(event.key() - 49))
                case Qt.Key_Right:
                    self.view.rows[self.view.num_row_enabled].select_neighbor_try_piece(Neighbor.RIGHT)
                case Qt.Key_Left:
                    self.view.rows[self.view.num_row_enabled].select_neighbor_try_piece(Neighbor.LEFT)
                case Qt.Key_Return | Qt.Key_Enter:
                    self.view.validate_combinaison()
