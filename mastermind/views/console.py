from mastermind.utils.parameters import RESET_COLOR


class Console:
    """Gère l'interface utilisateur en mode console"""
    @staticmethod
    def show_rules(preamble: str, colored_choices: list[str]) -> None:
        """Affichage des règles du jeu et du code couleur disponible"""
        print(f"{preamble}{f"    {RESET_COLOR}".join(colored_choices)}{RESET_COLOR}")

    @staticmethod
    def get_user_combination(try_number: int, max_tries: int, size_combination: int) -> str:
        """Obtient de l'utilisateur une combinaison"""
        return input(
            f"\nEssai {try_number}/{max_tries} - Veuillez saisir vos {size_combination} chiffres pour les couleurs : "
        )

    @staticmethod
    def show_result(combination: list[str], clues: list[str]) -> None:
        """Affiche la combinaison formatée de l'utilisateur suivi des indicateurs associés"""
        print(f"{" ".join(combination)}{RESET_COLOR} Indicateurs : {" ".join(clues)}{RESET_COLOR}")

    @staticmethod
    def show_game_over(sentence: str, combination: list[str]) -> None:
        """Affiche la phrase de fin de partie et la combinaison secrète"""
        print(f"{sentence}{" ".join(combination)}")

    @staticmethod
    def show_warning() -> None:
        """Affiche un message d'alerte"""
        print("Votre saisie est incorrecte...")
