from argparse import ArgumentParser
from sys import exit

from PySide6.QtWidgets import QApplication

from mastermind.controllers.console_controller import ConsoleController
from mastermind.controllers.window_controller import WindowController
from mastermind.model.game import Mastermind
from mastermind.model.settings import Config
from mastermind.utils.parameters import Level, Try, View
from mastermind.views.console import Console
from mastermind.views.main_window import MainWindow


def init_cli_parser(config: Config):
    """Initialisation du parser pour les options passées
    en ligne de commande au démarrage du script"""
    parser = ArgumentParser(
        prog="Mastermind UYS",
        description="Jeu de réflexion où le but est de deviner une combinaison de couleurs"
    )
    parser.add_argument('-m', '--mode',
                        choices=View.to_list(),
                        default=View.WINDOW.value,
                        help="Interface utilisateur")
    parser.add_argument('-l', '--level',
                        choices=Level.to_list(),
                        default=config.level.name.lower(),
                        help="Nombre de couleurs disponible")
    parser.add_argument('-t', '--tries',
                        choices=Try.to_list(),
                        default=config.tries.name.lower(),
                        help="Nombre d'essais maximum")
    return parser


def run_console(model: Mastermind, config: Config) -> None:
    """Lancement d'une partie en mode console"""
    view = Console()
    controller = ConsoleController(model, config, view)
    controller.run()


def run_window(model: Mastermind, config: Config) -> None:
    """Lancement d'une partie en mode fenêtré"""
    app = QApplication()
    view = MainWindow()
    controller = WindowController(model, config, view)
    controller.run()
    exit(app.exec())


def main() -> None:
    """Point d'entrée du programme"""
    config = Config()
    parser = init_cli_parser(config)
    args = parser.parse_args()
    config.level = Level.from_string(args.level)
    config.tries = Try.from_string(args.tries)
    model = Mastermind(config.level, config.tries)
    run_window(model, config) if View.from_string(args.mode) == View.WINDOW else run_console(model, config)


if __name__ == '__main__':
    main()
