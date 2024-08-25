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

    def load_ui(self):
        self.view.setup_ui(self.model.max_tries.value, self.model.level.value, self.model.secret_combinaison)

    def get_max_tries(self):
        return self.model.max_tries.value

    def get_secret_combination(self):
        return self.model.secret_combinaison

    def get_level(self):
        return self.model.level.value

    def is_game_over(self):
        return self.model.game_over

    def is_win(self):
        return self.model.win

    def evaluate_combination(self, combination: list[Color]):
        if (clues := self.model.evaluate_combinaison(combination)) is None:
            return
        self.view.display_clues(clues)
        self.view.deactivate_row()
        if self.is_game_over():
            self.view.display_game_over(self.is_win())
        else:
            self.view.activate_next_try()

    def run(self):
        self.load_ui()
        self.view.show()


if __name__ == '__main__':
    app = QApplication()
    m = Mastermind()
    v = MainWindow()
    c = WindowController(m, v)
    c.run()
    exit(app.exec())
