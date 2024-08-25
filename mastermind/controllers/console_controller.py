from mastermind.model.game import Mastermind
from mastermind.model.parameters import Color, SIZE_COMBINATION, SQUARE, DOT, PREAMBLE
from mastermind.views.console import Console


def convertion_color(colors: list[Color], symbol: str = None) -> list[str]:
    str_color, number, text = [], "", symbol
    for i, color in enumerate(colors, 1):
        red, green, blue = (int(color[j:j + 2], 16) for j in range(1, len(color), 2))
        if not symbol:
            number = f"[{i}] "
            text = color.name.capitalize()
        str_color.append(f"{number}\033[38;2;{red};{green};{blue}m{text}")
    return str_color


class ConsoleController:
    def __init__(self, model: Mastermind, view: Console) -> None:
        self.model = model
        self.view = view
        self.colors = {str(i): color for i, color in enumerate(self.model.available_colors, 1)}

    def build_colored_choices(self) -> list[str]:
        return convertion_color(self.model.available_colors)

    def run(self):
        self.view.show_rules(PREAMBLE, self.build_colored_choices())
        while not self.model.game_over:
            user_combination = self.view.get_user_combination(
                self.model.try_counter + 1,
                self.model.max_tries.value,
                SIZE_COMBINATION
            )
            colored_combination = [self.colors.get(char, Color.GRIS) for char in user_combination]
            evaluation = self.model.evaluate_combinaison(colored_combination)
            if evaluation is not None:
                self.view.show_result(convertion_color(colored_combination, SQUARE), convertion_color(evaluation, DOT))
            else:
                self.view.show_warning()
                continue

            if self.model.game_over:
                game_over_sentence = ("Bravo ! Vous avez trouvé la combinaison secrète : "
                                      if self.model.win
                                      else "Raté ! La combinaison secrète était : ")
                self.view.show_game_over(game_over_sentence, convertion_color(self.model.secret_combinaison, SQUARE))
                break


if __name__ == '__main__':
    m = Mastermind()
    v = Console()
    c = ConsoleController(m, v)
    print(c.model.secret_combinaison)
    c.run()
