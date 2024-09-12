from mastermind.model.game import Mastermind
from mastermind.utils.parameters import Color, SIZE_COMBINATION, SQUARE, DOT, get_help, View
from mastermind.views.console import Console


def convertion_color(colors: tuple[Color, ...], symbol: str = None) -> tuple[str, ...]:
    """Construit une liste de chaînes de caractères colorées (ANSI)"""
    str_color, number, text = [], "", symbol
    for i, color in enumerate(colors, 1):
        red, green, blue = color.to_rgb()
        if not symbol:
            number = f"[{i}] "
            text = color.name.capitalize()
        str_color.append(f"{number}\033[38;2;{red};{green};{blue}m{text}")
    return tuple(str_color)


class ConsoleController:
    def __init__(self, model: Mastermind, view: Console) -> None:
        self.model = model
        self.view = view
        self.colors = {str(i): color for i, color in enumerate(self.model.available_colors, 1)}

    def _get_user_combination(self) -> tuple[Color, ...]:
        """Obtient de l'utilisateur une combinaison.
        La retourne sous d'une liste de Color"""
        user_combination = self.view.get_user_combination(self.model.try_counter,
                                                          self.model.max_tries.value,
                                                          SIZE_COMBINATION)
        return tuple(self.colors.get(char, Color.GRIS) for char in user_combination)

    def _endgame(self) -> bool:
        """Si la partie est terminée, fait afficher à l'UI le résultat final"""
        if not self.model.game_over:
            return False
        game_over_sentence = ("Bravo ! Vous avez trouvé la combinaison secrète : "
                              if self.model.win
                              else "Raté ! La combinaison secrète était : ")
        self.view.show_game_over(game_over_sentence,
                                 convertion_color(self.model.secret_combination, SQUARE))
        return True

    def run(self) -> None:
        """Boucle du jeu"""
        self.view.show_rules(get_help(View.CONSOLE), convertion_color(self.model.available_colors))
        while True:
            colored_combination = self._get_user_combination()
            evaluation = self.model.evaluate_combinaison(colored_combination)
            if evaluation is not None:
                self.view.show_result(convertion_color(colored_combination, SQUARE), convertion_color(evaluation, DOT))
            else:
                self.view.show_warning()
                continue

            if self._endgame():
                break
