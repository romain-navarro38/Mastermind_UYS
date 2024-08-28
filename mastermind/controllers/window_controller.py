from sys import exit

from PySide6.QtWidgets import QApplication

from mastermind.model.game import Mastermind
from mastermind.model.parameters import Color
from mastermind.views.main_window import MainWindow


class WindowController:
    def __init__(self, model: Mastermind, view: MainWindow) -> None:
        self.model = model
        self.view = view
        self.view.evaluation_combination.connect(self.evaluate_combination)

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
            self.view.display_game_over(self.is_win())
        else:
            self.view.activate_next_try()

    def run(self) -> None:
        """Affiche la fenêtre principale"""
        self.load_ui()
        self.view.show()


if __name__ == '__main__':
    app = QApplication()
    m = Mastermind()
    v = MainWindow()
    c = WindowController(m, v)
    c.run()
    exit(app.exec())
