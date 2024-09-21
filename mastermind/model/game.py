from random import choice, shuffle

from mastermind.utils.parameters import Level, Color, Try, SIZE_COMBINATION


def shuffle_items_list(list_color: list) -> tuple:
    """Mélanger aléatoirement les éléments d'une liste donnée"""
    shuffle(list_color)
    return tuple(list_color)


class Mastermind:
    def __init__(self,
                 level: Level = Level.NORMAL,
                 tries_number: Try = Try.NORMAL) -> None:
        self.init_new_game(level, tries_number)

    @property
    def secret_combination(self) -> tuple[Color, ...]:
        """Retourne la combinaison secrète de la partie"""
        return self._secret

    def _generate_combinaison(self) -> tuple[Color, ...]:
        """Générer une liste de Color aléatoire"""
        return tuple(choice(self.available_colors) for _ in range(SIZE_COMBINATION))

    def _update_game_status(self, clues: list[Color]) -> None:
        """Met à jour le status de la partie (terminée ou non)
        et dans quel état (gagnée ou perdue)."""
        self.win = clues.count(Color.ROUGE) == SIZE_COMBINATION
        self.game_over = self.win or not self.remaining_tries

    def evaluate_combinaison(self, combination: tuple[Color, ...]) -> tuple[Color] | None:
        """Retourne une liste de Color représentant des indices déterminés en
        comparant la combinaison passée en paramètre et combinaison secrète."""
        if len(combination) == SIZE_COMBINATION and set(combination) <= set(self.available_colors):
            self.remaining_tries -= 1
            red = sum(s == c for s, c in zip(self._secret, combination, strict=False))
            white = sum(min(self._secret.count(c), combination.count(c)) for c in set(combination)) - red
            evaluation = [Color.ROUGE] * red + [Color.BLANC] * white
            self._update_game_status(evaluation)
            return shuffle_items_list(evaluation)

    def init_new_game(self, level: Level, max_tries: Try) -> None:
        """Initialiser les attributs pour commencer une nouvelle partie"""
        self.level = level
        self.max_tries = max_tries
        self.remaining_tries: int = max_tries.value
        self.game_over = self.win = False
        self.available_colors = tuple(Color)[:level.value]
        self._secret = self._generate_combinaison()
