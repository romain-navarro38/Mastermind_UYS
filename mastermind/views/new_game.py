from PySide6.QtWidgets import QLabel, QComboBox, QPushButton, QGridLayout, QDialog, QWidget

from mastermind.utils.dir import Dir, get_resource
from mastermind.utils.parameters import Level, Try


class NewGame(QDialog):
    """Fenêtre de paramétrage de la difficulté"""
    def __init__(self,
                 parent: QWidget,
                 old_level: Level = Level.NORMAL,
                 old_tries: Try = Try.NORMAL) -> None:
        super().__init__(parent)

        self.level = old_level
        self.tries = old_tries
        self._setup_ui()
        self.setStyleSheet(get_resource(Dir.STYLE / "qdialog.qss"))

    def _setup_ui(self) -> None:
        """Chargement, modification, disposition et connexion des composants"""
        self._setup_ui_create_widgets()
        self._setup_ui_modify_widgets()
        self._setup_ui_create_layouts()
        self._setup_ui_add_widgets_to_layouts()
        self._setup_ui_connections()
        self._setup_ui_translation()

    def _setup_ui_create_widgets(self) -> None:
        self.lab_description_level = QLabel()
        self.lab_description_try = QLabel()
        self.cb_level = QComboBox()
        self.cb_try = QComboBox()
        self.btn_exec = QPushButton()

    def _setup_ui_modify_widgets(self) -> None:
        for level in Level:
            self.cb_level.addItem(
                f"{self.parent().translation[level.name]} - {level.value} {self.parent().translation['colors']}",
                level
            )
        self.cb_level.setCurrentIndex(self.cb_level.findData(self.level))
        for tries in Try:
            self.cb_try.addItem(
                f"{self.parent().translation[tries.name]} - {tries.value} {self.parent().translation['tries']}",
                tries
            )
        self.cb_try.setCurrentIndex(self.cb_try.findData(self.tries))
        self.btn_exec.setObjectName("btn_green")

    def _setup_ui_create_layouts(self) -> None:
        self.main_layout = QGridLayout(self)

    def _setup_ui_add_widgets_to_layouts(self) -> None:
        self.main_layout.addWidget(self.lab_description_level, 0, 0, 1, 1)
        self.main_layout.addWidget(self.cb_level, 0, 1, 1, 1)
        self.main_layout.addWidget(self.lab_description_try, 1, 0, 1, 1)
        self.main_layout.addWidget(self.cb_try, 1, 1, 1, 1)
        self.main_layout.addWidget(self.btn_exec, 2, 0, 1, 2)

    def _setup_ui_connections(self) -> None:
        self.btn_exec.clicked.connect(self.accept)

    def _setup_ui_translation(self):
        self.setWindowTitle(self.parent().translation['new_game'])
        self.lab_description_level.setText(self.parent().translation['nb_colors_availables'])
        self.lab_description_try.setText(self.parent().translation['nb_max_tries'])
        self.btn_exec.setText(self.parent().translation['start'])

    def get_params_new_game(self) -> tuple[Level, Try]:
        """Retourne les instances Level et Try sélectionnées
        dans les QComboBox"""
        return self.cb_level.currentData(), self.cb_try.currentData()
