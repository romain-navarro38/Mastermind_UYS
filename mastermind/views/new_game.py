from PySide6.QtWidgets import QLabel, QComboBox, QPushButton, QGridLayout, QDialog, QWidget

from mastermind.utils.parameters import Level, Try, get_resource, STYLE_DIR


class NewGame(QDialog):
    """Fenêtre de paramétrage de la difficulté"""
    def __init__(self, parent: QWidget = None,
                 old_level: Level = Level.NORMAL,
                 old_tries: Try = Try.NORMAL) -> None:
        super().__init__(parent)
        self.level = old_level
        self.tries = old_tries
        self.setWindowTitle("Nouvelle partie")
        self.setup_ui()
        self.setStyleSheet(get_resource(STYLE_DIR / "style_qdialog.qss"))

    def setup_ui(self) -> None:
        """Chargement, modification, disposition et connexion des composants"""
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self) -> None:
        self.la_description_level = QLabel("Nombre de couleurs disponibles : ")
        self.la_description_try = QLabel("Nombre de tentatives maximum : ")
        self.cb_level = QComboBox()
        self.cb_try = QComboBox()
        self.btn_exec = QPushButton("Lancer")

    def modify_widgets(self) -> None:
        for level in Level:
            self.cb_level.addItem(f"{level} - {level.value} couleurs", level)
        self.cb_level.setCurrentIndex(self.cb_level.findData(self.level))
        for tries in Try:
            self.cb_try.addItem(f"{tries} - {tries.value} essais", tries)
        self.cb_try.setCurrentIndex(self.cb_try.findData(self.tries))
        self.btn_exec.setObjectName("btn_green")

    def create_layouts(self) -> None:
        self.main_layout = QGridLayout(self)

    def add_widgets_to_layouts(self) -> None:
        self.main_layout.addWidget(self.la_description_level, 0, 0, 1, 1)
        self.main_layout.addWidget(self.cb_level, 0, 1, 1, 1)
        self.main_layout.addWidget(self.la_description_try, 1, 0, 1, 1)
        self.main_layout.addWidget(self.cb_try, 1, 1, 1, 1)
        self.main_layout.addWidget(self.btn_exec, 2, 0, 1, 2)

    def setup_connections(self) -> None:
        self.btn_exec.clicked.connect(self.accept)

    def get_params_new_game(self) -> tuple[Level, Try]:
        """Retourne les instances Level et Try sélectionnées
        dans les QComboBox"""
        return self.cb_level.currentData(), self.cb_try.currentData()
