from mastermind.model.game import Mastermind
from mastermind.utils.parameters import Color, SIZE_COMBINATION, SQUARE, DOT, View, Config
from mastermind.views.console import Console


class ConsoleController:
    def __init__(self, model: Mastermind, config: Config, view: Console) -> None:
        self.model = model
        self.config = config
        self.view = view
        self.colors = {str(i): color for i, color in enumerate(self.model.available_colors, 1)}

    def _convertion_color(self, colors: tuple[Color, ...], symbol: str = None) -> tuple[str, ...]:
        """Construit une liste de chaînes de caractères colorées (ANSI)"""
        str_color, number, text = [], "", symbol
        for i, color in enumerate(colors, 1):
            red, green, blue = color.to_rgb()
            if not symbol:
                number = f"[{i}]"
                text = self.model.get_text(self.config.language, color.name).capitalize()
            str_color.append(f"{number} \033[38;2;{red};{green};{blue}m{text}")
        return tuple(str_color)

    def _endgame(self) -> bool:
        """Si la partie est terminée, fait afficher à l'UI le résultat final"""
        if not self.model.game_over:
            return False
        game_over_sentence = (self.model.get_text(self.config.language, "win_console")
                              if self.model.win
                              else self.model.get_text(self.config.language, "lose_console"))
        self.view.show_game_over(game_over_sentence,
                                 self._convertion_color(self.model.secret_combination, SQUARE))
        return True

    def _get_user_combination(self) -> tuple[Color, ...]:
        """Obtient de l'utilisateur une combinaison.
        La retourne sous forme d'un tuple de Color"""
        try_number = self.model.max_tries.value - self.model.remaining_tries + 1
        sentence = self.model.get_text(self.config.language, "input_user").format(
            try_number=try_number,
            max_tries=self.model.max_tries.value,
            size_combination=SIZE_COMBINATION
        )
        user_combination = self.view.get_user_combination(sentence)
        return tuple(self.colors.get(char, Color.GRAY) for char in user_combination)

    def run(self) -> None:
        """Boucle du jeu"""
        self.view.show_rules(self.model.get_help(View.CONSOLE, self.config.language),
                             self._convertion_color(self.model.available_colors))
        while True:
            colored_combination = self._get_user_combination()
            evaluation = self.model.evaluate_combinaison(colored_combination)
            if evaluation is not None:
                self.view.show_result(self._convertion_color(colored_combination, SQUARE),
                                      self._convertion_color(evaluation, DOT),
                                      self.model.get_text(self.config.language, "clue"))
            else:
                self.view.show_warning(self.model.get_text(self.config.language, "warning"))
                continue

            if self._endgame():
                break
