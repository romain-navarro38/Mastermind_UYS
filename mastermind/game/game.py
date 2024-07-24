from random import choice

from mastermind.game.parameter import Level, Color, Try, SIZE_COMBINATION


class Mastermind:
    def __init__(self,
                 level: Level = Level.NORMAL,
                 tries_number: Try = Try.NORMAL):
        self.level = level
        self.max_tries = tries_number
        self.try_counter = 0
        self.game_over = self.win = False
        self.available_colors = [color for color in Color][:self.level.value]
        self.secret_combinaison = self.generate_combinaison()

    def generate_combinaison(self) -> list[Color]:
        """Génére une liste de Color aléatoire"""
        return [choice(self.available_colors) for _ in range(SIZE_COMBINATION)]

    def evaluate_combinaison(self, combination: list[Color]) -> list[Color] | None:
        """Merci à @Mack pour cet algorithme qui m'a bien simplifié la méthode.
        Retourne une liste de Color représentant des indices déterminés en
        comparant la combinaison passée en paramètre et combinaison secrète."""
        # evaluation = []
        # secret = self.secret_combinaison.copy()
        # for i, elem in enumerate(combinaison):
        #     if elem == secret[i]:
        #         evaluation.append(Color.RED)
        #         secret[i] = Color.UNDEFINED
        #         combinaison[i] = None
        #
        # for elem in combinaison:
        #     if elem in secret:
        #         evaluation.append(Color.WHITE)
        #         secret.remove(elem)
        #
        # self.check_game_over(evaluation)
        # return evaluation

        if len(combination) == SIZE_COMBINATION and set(combination) <= set(self.available_colors):
            self.try_counter += 1
            red = sum(1 for s, c in zip(self.secret_combinaison, combination, strict=False) if s == c)
            white = sum(min(self.secret_combinaison.count(c), combination.count(c)) for c in set(combination)) - red
            evaluation = [Color.RED] * red + [Color.WHITE] * white
            self.check_game_over(evaluation)
            return evaluation
        return

    def check_game_over(self, clues: list[Color]):
        """Détermine si la partie est terminée ou non
        et dans quel état (gagné ou perdu)."""
        self.win = clues.count(Color.RED) == SIZE_COMBINATION
        self.game_over = self.win or self.try_counter == self.max_tries.value


if __name__ == '__main__':
    m = Mastermind(Level.DIFFICULT)
    print(f"secret : {m.secret_combinaison}")
    e = m.generate_combinaison()
    # e = [Color.GREEN, Color.GREEN, Color.RED, Color.RED]
    print(f"proposé : {e}")
    print(f"sortie : {m.evaluate_combinaison(e)}")
    # print(e)
