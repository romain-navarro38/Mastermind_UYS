from mastermind.model.parameters import RESET_COLOR


class Console:
    @staticmethod
    def show_rules(preamble: str, colored_choices: list[str]) -> None:
        print(f"{preamble}{f"    {RESET_COLOR}".join(colored_choices)}{RESET_COLOR}")

    @staticmethod
    def get_user_combination(try_number: int, max_tries: int, size_combination: int) -> str:
        return input(
            f"\nEssai {try_number}/{max_tries} - Veuillez saisir vos {size_combination} chiffres pour les couleurs : "
        )

    @staticmethod
    def show_result(combination: list[str], clues: list[str]) -> None:
        print(f"{" ".join(combination)}{RESET_COLOR} Indicateurs : {" ".join(clues)}{RESET_COLOR}")

    @staticmethod
    def show_game_over(sentence: str, combination: list[str]) -> None:
        print(f"{sentence}{" ".join(combination)}")

    @staticmethod
    def show_warning() -> None:
        print("Votre saisie est incorrecte...")
