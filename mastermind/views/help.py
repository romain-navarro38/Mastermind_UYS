from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QWidget, QTextBrowser, QVBoxLayout, QScrollArea

from mastermind.utils.parameters import get_resource, DIRECTORIES
from mastermind.views.custom_widget import CustomButton


class HelpWindow(QWidget):
    """Fenêtre d'affichage de l'aide"""
    def __init__(self, translation: dict) -> None:
        super().__init__()

        self.translation = translation
        self._setup_ui()
        self.resize(600, 500)
        self.setWindowIcon((QIcon(QPixmap(DIRECTORIES['icon'] / "logo.png"))))
        self.setStyleSheet(get_resource(DIRECTORIES['style'] / "help.qss"))

    def _setup_ui(self) -> None:
        self._setup_ui_create_widgets()
        self._setup_ui_modify_widgets()
        self._setup_ui_create_layouts()
        self._setup_ui_add_widgets_to_layouts()
        self._setup_ui_connections()
        self._setup_ui_translation()

    def _setup_ui_create_widgets(self) -> None:
        self.scroll_area = QScrollArea()
        self.text_browser = QTextBrowser()
        self.btn_close = CustomButton()

    def _setup_ui_modify_widgets(self) -> None:
        pass

    def _setup_ui_create_layouts(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.scroll_layout = QVBoxLayout()

    def _setup_ui_add_widgets_to_layouts(self) -> None:
        self.main_layout.addLayout(self.scroll_layout)
        self.scroll_layout.addWidget(self.text_browser)
        self.main_layout.addWidget(self.btn_close)

    def _setup_ui_connections(self) -> None:
        self.btn_close.clicked.connect(self.close)

    def _setup_ui_translation(self) -> None:
        self.setWindowTitle(self.translation['window_title'])
        self.btn_close.setText(self.translation['close_button'])
        self.text_browser.setText(self.translation['help'])
