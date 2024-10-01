from enum import Enum, StrEnum, auto
from json import load, JSONDecodeError, dump
from jsonschema import validate, ValidationError
from typing import Self

from .dir import Dir

SIZE_COMBINATION = 4
SQUARE = "\u25A0"  # correspondant à ■
DOT = "\u25CF"  # correspondant à ●
RESET_COLOR = "\033[0m"


class Color(StrEnum):
    """Classe StrEnum représentant une couleur
    associé à son code hexadécimal"""
    YELLOW = '#ffff00'
    BLUE = '#0000ff'
    RED = '#ff0000'
    GREEN = '#00ff00'
    WHITE = '#ffffff'
    MAGENTA = '#ff00ff'
    CYAN = '#00ffff'
    BROWN = '#906434'
    BLACK = "#000000"
    GRAY = '#7f7f7f'

    @classmethod
    def from_index(cls, index: int) -> Self:
        """Retourne l'instance correspondant à l'index donné"""
        return list(cls)[index]

    def get_opposite(self) -> str:
        """Retourne la couleur opposée au format hexadécimal"""
        return f"#{''.join([f'{hex(255 - c)[2:]:02}' for c in self.to_rgb()])}"

    def to_rgb(self) -> tuple[int, ...]:
        """Retourne la couleur au format RGB"""
        return tuple(int(self.value[i:i + 2], 16) for i in range(1, len(self.value), 2))


class Language(StrEnum):
    FR = 'FR'
    EN = 'EN'

    @classmethod
    def to_list(cls) -> list[str]:
        return list(attribute.value for attribute in cls)

    @classmethod
    def from_string(cls, name: str) -> Self:
        """Retourne l'instance correspondant au nom donné"""
        return next(attribute for attribute in cls if attribute.name == name)


class Level(Enum):
    """Classe Enum représentant le nombre de couleurs disponible
    pour composer une combinaison"""
    EASY = 4
    NORMAL = 6
    HARD = 8

    def __str__(self):
        return self.name.lower()

    @classmethod
    def from_string(cls, name: str) -> Self:
        """Retourne l'instance correspondant au nom donné"""
        return next(attribute for attribute in cls if attribute.name.lower() == name.lower())

    @classmethod
    def to_list(cls) -> list[str]:
        """Retourne la liste de tous les attributs au format str"""
        return list(str(attribute) for attribute in cls)


class Neighbor(Enum):
    """Classe Enum représentant le pion voisin,
    à droite ou à gauche, dans une ligne d'essai"""
    RIGHT = auto()
    LEFT = auto()


class Try(Enum):
    """Classe Enum représentant le nombre maximum d'essais
    pour trouver la combinaison secrète"""
    EASY = 12
    NORMAL = 10

    def __str__(self):
        return self.name.lower()

    @classmethod
    def from_string(cls, name: str) -> Self:
        """Retourne l'instance correspondant au nom donné"""
        return next(attribute for attribute in cls if attribute.name.lower() == name)

    @classmethod
    def to_list(cls) -> list[str]:
        """Retourne la liste de tous les attributs au format str"""
        return list(str(attribute) for attribute in cls)


class Config:
    """Gestion via un fichier json de paramètres"""
    _DEFAULT_CONFIG = {'language': 'FR', 'level': 'normal', 'tries': 'normal'}

    def __init__(self):
        self._schema = {
            "type": "object",
            "properties": {
                "language": {"enum": Language.to_list()},
                "level": {"enum": Level.to_list()},
                "tries": {"enum": Try.to_list()},
            },
            "required": ["language", "level", "tries"]
        }
        self._config = self._get_config()

    @staticmethod
    def _set_config(config: dict) -> None:
        """Stockage du paramètrage en json"""
        with open(Dir.ROOT / "config.json", 'w', encoding='utf-8') as file:
            dump(config, file, indent=4)

    @property
    def language(self) -> Language:
        return Language.from_string(self._config["language"])

    @language.setter
    def language(self, value: Language) -> None:
        if not isinstance(value, Language):
            raise ValueError("")
        self._config["language"] = value.name
        self._set_config(self._config)

    @property
    def level(self) -> Level:
        return Level.from_string(self._config["level"])

    @level.setter
    def level(self, value: Level) -> None:
        if not isinstance(value, Level):
            raise ValueError("")
        self._config["level"] = value.name.lower()
        self._set_config(self._config)

    @property
    def tries(self) -> Try:
        return Try.from_string(self._config["tries"])

    @tries.setter
    def tries(self, value: Try) -> None:
        if not isinstance(value, Try):
            raise ValueError("")
        self._config["tries"] = value.name.lower()
        self._set_config(self._config)

    def _check_json(self, data) -> bool:
        """Validation des données"""
        try:
            validate(instance=data, schema=self._schema)
        except ValidationError as e:
            print(f"Erreur de validation: {e}")
            return False
        return True

    def _get_config(self) -> dict:
        """Si valide, retourne le paramètrage stocké dans le fichier config.json.
        Sinon le paramètrage par défaut"""
        try:
            with open(Dir.ROOT / "config.json", 'r', encoding='utf-8') as file:
                config: dict = load(file)
        except JSONDecodeError as e:
            print(f"Erreur de décodage JSON: {e}")
        except FileNotFoundError as e:
            print(f"Fichier non trouvé: {e}")
        except Exception as e:
            print(f"Une erreur est survenue: {e}")
        else:
            if self._check_json(config):
                return config
        self._set_config(Config._DEFAULT_CONFIG)
        return Config._DEFAULT_CONFIG


class View(StrEnum):
    """Classe StrEnum représentant une vue"""
    CONSOLE = 'console'
    WINDOW = 'window'

    @classmethod
    def from_string(cls, name: str) -> Self:
        """Retourne l'instance correspondant au nom donné"""
        return next(attribute for attribute in cls if attribute.value == name)

    @classmethod
    def to_list(cls) -> list[str]:
        """Retourne la liste de tous les attributs au format str"""
        return list(attribute.value for attribute in cls)
