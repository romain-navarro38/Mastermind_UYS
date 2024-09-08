import argparse
from sys import exit

from PySide6.QtWidgets import QApplication

from mastermind.controllers.console_controller import ConsoleController
from mastermind.controllers.window_controller import WindowController
from mastermind.model.game import Mastermind
from mastermind.utils.parameters import Level, Try, View
from mastermind.views.console import Console
from mastermind.views.main_window import MainWindow


def init_cli_parser():
    """Initialisation du parser pour les options passées
    en ligne de commande au démarrage du script"""
    parser = argparse.ArgumentParser(
        prog="Mastermind UYS",
        description="Jeu de réflexion où le but est de deviner une combinaison de couleurs"
    )
    parser.add_argument('-m', '--mode',
                        choices=View.to_list(),
                        default=View.WINDOW.value,
                        help="Interface utilisateur")
    parser.add_argument('-l', '--level',
                        choices=list(str(level) for level in Level),
                        default=Level.NORMAL.name.lower(),
                        help="Nombre de couleurs disponible")
    parser.add_argument('-t', '--tries',
                        choices=list(str(tries) for tries in Try),
                        default=Try.NORMAL.name.lower(),
                        help="Nombre d'essais maximum")
    return parser


def run_console(model: Mastermind) -> None:
    """Lancement d'une partie en mode console"""
    view = Console()
    controller = ConsoleController(model, view)
    controller.run()


def run_window(model: Mastermind) -> None:
    """Lancement d'une partie en mode fenêtré"""
    app = QApplication()
    view = MainWindow()
    controller = WindowController(model, view)
    controller.run()
    exit(app.exec())


def main() -> None:
    """Point d'entrée du programme"""
    parser = init_cli_parser()
    args = parser.parse_args()
    model = Mastermind(Level.from_string(args.level),
                       Try.from_string(args.tries))
    run_console(model) if View.from_string(args.mode) == View.CONSOLE else run_window(model)


if __name__ == '__main__':
    main()
