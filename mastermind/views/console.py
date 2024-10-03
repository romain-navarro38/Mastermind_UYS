from mastermind.model.settings import RESET_COLOR


class Console:
    """Gère l'interface utilisateur en mode console"""
    @staticmethod
    def get_user_combination(sentence: str) -> str:
        """Obtient de l'utilisateur une combinaison"""
        return input(f"\n{sentence} ")

    @staticmethod
    def show_game_over(sentence: str, combination: tuple[str, ...]) -> None:
        """Affiche la phrase de fin de partie et la combinaison secrète"""
        print(f"{sentence} {" ".join(combination)}")

    @staticmethod
    def show_result(combination: tuple[str, ...], clues: tuple[str, ...], indicator: str) -> None:
        """Affiche la combinaison formatée de l'utilisateur suivi des indicateurs associés"""
        print(f"{" ".join(combination)}{RESET_COLOR} {indicator} {" ".join(clues)}{RESET_COLOR}")

    @staticmethod
    def show_rules(preamble: str, colored_choices: tuple[str, ...]) -> None:
        """Affichage des règles du jeu et du code couleur disponible"""
        print(f"{preamble}{f"    {RESET_COLOR}".join(colored_choices)}{RESET_COLOR}")

    @staticmethod
    def show_warning(sentence: str) -> None:
        """Affiche un message d'alerte"""
        print(sentence)
