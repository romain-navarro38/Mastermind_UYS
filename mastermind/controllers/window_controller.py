from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

from mastermind.model.game import Mastermind
from mastermind.utils.parameters import Color, Neighbor
from mastermind.views.main_window import MainWindow
from mastermind.views.new_game import NewGame
from mastermind.views.help import HelpWindow


class WindowController:
    def __init__(self, model: Mastermind, view: MainWindow) -> None:
        self.model = model
        self.view = view

    def _init_reception_signal(self) -> None:
        """Connexion des signaux de la vue"""
        self.view.evaluation_combination.connect(self._evaluate_combination)
        self.view.event_keyboard.connect(self._parse_input)
        self.view.restart.connect(self._new_game)
        self.view.show_rules.connect(self._show_rules)

    def _load_ui(self) -> None:
        """Chargement des composants de la fenêtre"""
        self.view.setup_ui(self.model.max_tries.value, self.model.level.value, self.model.secret_combination)

    def _is_game_over(self) -> bool:
        """Retourne True si la partie est terminée"""
        return self.model.game_over

    def _is_win(self) -> bool:
        """Retourne True si la partie est gagnée"""
        return self.model.win

    def _evaluate_combination(self, combination: tuple[Color]) -> None:
        """Obtient du modèle les indices associés à la combinaison évaluée
        et met à jour la vue en conséquence"""
        if (clues := self.model.evaluate_combinaison(combination)) is None:
            return
        self.view.display_clues(clues)
        self.view.deactivate_row()
        if self._is_game_over():
            self.view.game_in_progress = False
            self.view.display_game_over(self._is_win())
        else:
            self.view.game_in_progress = True
            self.view.activate_next_try()

    def run(self) -> None:
        """Affiche la fenêtre principale"""
        self._load_ui()
        self._init_reception_signal()
        self.view.show()

    def _parse_input(self, event: QKeyEvent) -> None:
        """Déclenche, sur la vue, l'action associée à l'entrée clavier"""
        if event.modifiers() == Qt.ControlModifier:
            match event.key():
                case Qt.Key_Q:
                    self.view.close()
                case Qt.Key_N:
                    self._new_game()
                case Qt.Key_R:
                    self._show_rules()
        elif not self._is_game_over():
            match event.key():
                case num if 49 <= num <= 48 + self.model.level.value:
                    self.view.positioned_color(Color.from_index(event.key() - 49))
                case Qt.Key_Right:
                    self.view.rows[self.view.num_row_enabled].select_neighbor_try_piece(Neighbor.RIGHT)
                case Qt.Key_Left:
                    self.view.rows[self.view.num_row_enabled].select_neighbor_try_piece(Neighbor.LEFT)
                case Qt.Key_Return | Qt.Key_Enter:
                    self.view.validate_combinaison()

    def _new_game(self) -> None:
        """Chargement d'une nouvelle fenêtre de jeu"""
        if self.view.game_in_progress and not self.view.confirmation_interruption():
            return
        dialog = NewGame(self.view, self.model.level, self.model.max_tries)
        if dialog.exec():
            level, tries = dialog.get_params_new_game()
            self.model.init_new_game(level, tries)
            self._close_view()
            self.view = MainWindow()
            self.run()

    def _close_view(self) -> None:
        """Fermeture de la fenêtre de jeu"""
        self.view.game_in_progress = False
        self.view.close()

    def _show_rules(self) -> None:
        self.rules = HelpWindow()
        self.rules.setWindowModality(Qt.ApplicationModal)
        self.rules.show()
