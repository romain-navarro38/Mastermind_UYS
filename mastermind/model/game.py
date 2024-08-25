from random import choice, shuffle

from mastermind.model.parameters import Level, Color, Try, SIZE_COMBINATION


def shuffle_items_list(list_color: list[Color]) -> list[Color]:
    shuffle(list_color)
    return list_color


class Mastermind:
    def __init__(self,
                 level: Level = Level.NORMAL,
                 tries_number: Try = Try.NORMAL) -> None:
        self.level = level
        self.max_tries = tries_number
        self.try_counter = 0
        self.game_over = self.win = False
        self.available_colors = list(Color)[:self.level.value]
        self.secret_combinaison = self.generate_combinaison()

    def generate_combinaison(self) -> list[Color]:
        """Génère une liste de Color aléatoire"""
        return [choice(self.available_colors) for _ in range(SIZE_COMBINATION)]

    def evaluate_combinaison(self, combination: list[Color]) -> list[Color] | None:
        """Retourne une liste de Color représentant des indices déterminés en
        comparant la combinaison passée en paramètre et combinaison secrète."""
        if len(combination) == SIZE_COMBINATION and set(combination) <= set(self.available_colors):
            self.try_counter += 1
            red = sum(
                s == c
                for s, c in zip(self.secret_combinaison, combination, strict=False)
            )
            white = sum(min(self.secret_combinaison.count(c), combination.count(c)) for c in set(combination)) - red
            evaluation = [Color.ROUGE] * red + [Color.BLANC] * white
            self.update_game_status(evaluation)
            return shuffle_items_list(evaluation)
        return

    def update_game_status(self, clues: list[Color]) -> None:
        """Met à jour le status de la partie (terminée ou non)
        et dans quel état (gagné ou perdu)."""
        self.win = clues.count(Color.ROUGE) == SIZE_COMBINATION
        self.game_over = self.win or self.try_counter == self.max_tries.value


if __name__ == '__main__':
    pass
