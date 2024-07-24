import sys

from PySide6.QtWidgets import QApplication

from mastermind.game.game import Mastermind
from mastermind.window.main_window import MainWindow


def main():
    app = QApplication()
    window = MainWindow(Mastermind())
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

# TODO:
#  - Fenêtre règles du jeu
#  - Mode console
#  - Lancement du script avec option fenêtre ou console (par défaut fenêtre) avec argparse
#  - Possibilité changement difficulté (nombre d'essai, nombre de couleur)
#  - Proposer de recommencer une partie
