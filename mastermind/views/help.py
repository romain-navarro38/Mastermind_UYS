from PySide6.QtWidgets import QWidget, QTextBrowser, QVBoxLayout, QScrollArea

from mastermind.utils.parameters import get_resource, get_help, DIRECTORIES, View
from mastermind.views.custom_widget import CustomButton


class HelpWindow(QWidget):
    """Fenêtre d'affichage de l'aide"""
    def __init__(self) -> None:
        super().__init__()

        self._setup_ui()
        self.resize(600, 500)
        self.setWindowTitle("Aide")
        self.setStyleSheet(get_resource(DIRECTORIES['style'] / "help.qss"))

    def _setup_ui(self) -> None:
        self._setup_ui_create_widgets()
        self._setup_ui_modify_widgets()
        self._setup_ui_create_layouts()
        self._setup_ui_add_widgets_to_layouts()
        self._setup_ui_connections()

    def _setup_ui_create_widgets(self) -> None:
        self.scroll_area = QScrollArea()
        self.text_browser = QTextBrowser()
        self.btn_close = CustomButton("Fermer")

    def _setup_ui_modify_widgets(self) -> None:
        self.text_browser.setText(get_help(View.WINDOW))

    def _setup_ui_create_layouts(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.scroll_layout = QVBoxLayout()

    def _setup_ui_add_widgets_to_layouts(self) -> None:
        self.main_layout.addLayout(self.scroll_layout)
        self.scroll_layout.addWidget(self.text_browser)
        self.main_layout.addWidget(self.btn_close)

    def _setup_ui_connections(self) -> None:
        self.btn_close.clicked.connect(self.close)
