from mastermind.game.game import Mastermind
from mastermind.game.parameter import SIZE_COMBINATION, Color

PREAMBLE = f"""JEU DU MASTERMIND
Trouver la bonne combinaison de {SIZE_COMBINATION} couleurs secrètes que notre 'IA' aura généré.
A chaque couleur bien positionnée, vous aurez en retour un indicateur rouge.
A chaque couleur présente mais mal positionnée, vous aurez en retour un indicateur blanc.

Entrez votre combinaison secrète en utilisant les chiffres des couleurs disponibles.
"""
CARRE = "\u25A0"  # correspondant à ■
PASTILLE = "\u25CF"  # correspondant à ●
RESET_COLOR = "\033[0m"


def convertion_color(colors: list[Color], symbole: str) -> str:
    str_color = []
    for color in colors:
        red, green, blue = (int(color[j:j + 2], 16) for j in range(1, len(color), 2))
        str_color.append(f"\033[38;2;{red};{green};{blue}m{symbole}")
    return " ".join(str_color)


class Console:
    def __init__(self, mastermind: Mastermind) -> None:
        self.mastermind = mastermind
        self.colors = {str(i): color for i, color in enumerate(self.mastermind.available_colors, 1)}

    def show_rules(self) -> None:
        colored_choices = []
        for i, color in enumerate(self.mastermind.available_colors, 1):
            red, green, blue = (int(color[j:j + 2], 16) for j in range(1, len(color), 2))
            colored_choices.append(f"[{i}]: \033[38;2;{red};{green};{blue}m{color.name.capitalize()}")
        print(f"{PREAMBLE}{f"    {RESET_COLOR}".join(colored_choices)}{RESET_COLOR}")

    def run(self):
        while self.mastermind.try_counter < self.mastermind.max_tries.value:
            user_choice = input(
                f"\nEssai {self.mastermind.try_counter + 1}/{self.mastermind.max_tries.value} - Veuillez saisir vos {SIZE_COMBINATION} chiffres pour les couleurs : ")
            d = [self.colors.get(char, Color.GRAY) for char in user_choice]
            evaluation = self.mastermind.evaluate_combinaison(d)
            if evaluation is not None:
                print(f"{convertion_color(d, CARRE)}{RESET_COLOR} Indicateurs : {convertion_color(evaluation, PASTILLE)}{RESET_COLOR}")
            else:
                print("Votre saisie est incorrecte...")
                continue

            if self.mastermind.game_over:
                game_over_sentence = ("Bravo ! Vous avez trouvé la combinaison secrète : "
                                      if self.mastermind.win
                                      else "Raté ! La combinaison secrète était : ")
                print(f"{game_over_sentence}{convertion_color(self.mastermind.secret_combinaison, CARRE)}")
                break


if __name__ == '__main__':
    c = Console(Mastermind())
    c.show_rules()
    c.run()
