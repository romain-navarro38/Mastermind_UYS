from json import JSONDecodeError, load, dump

from jsonschema import validate, ValidationError

from mastermind.utils.dir import Dir
from mastermind.utils.logger import setup_logger
from mastermind.utils.parameters import Level, Try, Language

SIZE_COMBINATION = 4
SQUARE = "\u25A0"  # correspondant à ■
DOT = "\u25CF"  # correspondant à ●
RESET_COLOR = "\033[0m"


class Config:
    """Gestion via un fichier json de paramètres"""
    _DEFAULT_CONFIG = {'language': 'FR', 'level': 'normal', 'tries': 'normal'}
    log = setup_logger("config")

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
            Config.log.error(f"JSON decoding error: {e}")
        except FileNotFoundError as e:
            Config.log.error(f"Configuration file not found: {e}")
        except Exception as e:
            Config.log.error(f"An error has occurred: {e}")
        else:
            if self._check_json(config):
                return config
        self._set_config(Config._DEFAULT_CONFIG)
        Config.log.info("Restored configuration file")
        return Config._DEFAULT_CONFIG
