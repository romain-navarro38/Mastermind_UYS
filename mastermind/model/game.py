from random import choice, shuffle

from mastermind.model.language import LANGUAGE
from mastermind.utils.parameters import Level, Color, Try, SIZE_COMBINATION, Language, View, get_resource, DIRECTORIES


def shuffle_items_list(list_color: list) -> tuple:
    """Mélanger aléatoirement les éléments d'une liste donnée"""
    shuffle(list_color)
    return tuple(list_color)


class Mastermind:
    def __init__(self, level: Level, tries_number: Try) -> None:
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
        self.win = clues.count(Color.RED) == SIZE_COMBINATION
        self.game_over = self.win or not self.remaining_tries

    def evaluate_combinaison(self, combination: tuple[Color, ...]) -> tuple[Color] | None:
        """Retourne une liste de Color représentant des indices déterminés en
        comparant la combinaison passée en paramètre et combinaison secrète."""
        if len(combination) == SIZE_COMBINATION and set(combination) <= set(self.available_colors):
            self.remaining_tries -= 1
            red = sum(s == c for s, c in zip(self._secret, combination, strict=False))
            white = sum(min(self._secret.count(c), combination.count(c)) for c in set(combination)) - red
            evaluation = [Color.RED] * red + [Color.WHITE] * white
            self._update_game_status(evaluation)
            return shuffle_items_list(evaluation)

    @staticmethod
    def get_text(language: Language, key: str) -> str:
        """Retourne un texte dans la langue demandée"""
        return LANGUAGE[language][key]

    def get_help(self, mode: View, language: Language) -> str:
        """Retourne le texte d'aide à afficher en fonction de la vue"""
        start_h1 = end_h1 = start_paragraph = end_paragraph = return_line = ""
        if mode == View.WINDOW:
            start_h1, end_h1 = "<h1>", "</h1>"
            start_paragraph, end_paragraph = "<p>", "</p>"
            return_line = "<br />"
        preamble = self.get_text(language, "preamble").format(
            start_h1=start_h1, end_h1=end_h1,
            start_paragraph=start_paragraph, end_paragraph=end_paragraph,
            return_line=return_line, SIZE_COMBINATION=SIZE_COMBINATION
        )
        html = f"help_{language.name}.html"
        return (f"{preamble}\n\n{self.get_text(language, "choose_color")}\n"
                if mode == View.CONSOLE else
                f"{preamble}\n{get_resource(DIRECTORIES['html'] / html)}")

    def init_new_game(self, level: Level, max_tries: Try) -> None:
        """Initialiser les attributs pour commencer une nouvelle partie"""
        self.level = level
        self.max_tries = max_tries
        self.remaining_tries: int = self.max_tries.value
        self.game_over = self.win = False
        self.available_colors = tuple(Color)[:self.level.value]
        self._secret = self._generate_combinaison()
