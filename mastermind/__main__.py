import sys

from PySide6.QtWidgets import QApplication

from mastermind.controllers.console_controller import ConsoleController
from mastermind.controllers.window_controller import WindowController
from mastermind.model.game import Mastermind
from mastermind.views.main_window import MainWindow


def main():
    app = QApplication()
    model = Mastermind()
    view = MainWindow()
    controller = WindowController(model, view)
    controller.run()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

# TODO:
#  - Fenêtre règles du jeu
#  - Mode console
#  - Lancement du script avec option fenêtre ou console (par défaut fenêtre) avec argparse
#  - Possibilité changement difficulté (nombre d'essai, nombre de couleur)
#  - Proposer de recommencer une partie
