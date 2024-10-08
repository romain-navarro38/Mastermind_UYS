from PySide6.QtWidgets import QWidget, QDialog, QLabel, QDialogButtonBox, QVBoxLayout

from mastermind.utils.dir import Dir, get_resource


class ConfirmationMessage(QDialog):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self._setup_ui()
        self.setStyleSheet(get_resource(Dir.STYLE / "qdialog.qss"))
        self.btn_no.setFocus()

    def _setup_ui(self):
        """Chargement, modification, disposition et connexion des composants"""
        self._setup_ui_create_widgets()
        self._setup_ui_modify_widgets()
        self._setup_ui_create_layouts()
        self._setup_ui_add_widgets_to_layouts()
        self._setup_ui_connections()
        self._setup_ui_translation()

    def _setup_ui_create_widgets(self):
        self.lab_message = QLabel()
        self.btn_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        self.btn_yes = self.btn_box.button(QDialogButtonBox.Yes)
        self.btn_no = self.btn_box.button(QDialogButtonBox.No)

    def _setup_ui_modify_widgets(self):
        self.btn_yes.setObjectName("btn_red")
        self.btn_no.setObjectName("btn_green")

    def _setup_ui_create_layouts(self):
        self.layout = QVBoxLayout()

    def _setup_ui_add_widgets_to_layouts(self):
        self.layout.addWidget(self.lab_message)
        self.layout.addWidget(self.btn_box)
        self.setLayout(self.layout)

    def _setup_ui_connections(self):
        self.btn_box.accepted.connect(self.accept)
        self.btn_box.rejected.connect(self.reject)

    def _setup_ui_translation(self):
        self.setWindowTitle(self.parent().translation['confirmation_title'])
        self.lab_message.setText(self.parent().translation['message_confirmation'])
        self.btn_yes.setText(self.parent().translation['yes'])
        self.btn_no.setText(self.parent().translation['no'])
