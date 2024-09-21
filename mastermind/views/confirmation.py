from PySide6.QtWidgets import QWidget, QDialog, QLabel, QDialogButtonBox, QVBoxLayout

from mastermind.utils.parameters import get_resource, DIRECTORIES


class ConfirmationMessage(QDialog):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setWindowTitle("Confirmation")
        self._setup_ui()
        self.setStyleSheet(get_resource(DIRECTORIES['style'] / "qdialog.qss"))
        self.btn_no.setFocus()

    def _setup_ui(self):
        self._setup_ui_create_widgets()
        self._setup_ui_modify_widgets()
        self._setup_ui_create_layouts()
        self._setup_ui_add_widgets_to_layouts()
        self._setup_ui_connections()

    def _setup_ui_create_widgets(self):
        self.lab_message = QLabel("Une partie est en cours !\nVoulez-vous vraiment l'arrêter ?")
        self.btn_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        self.btn_yes = self.btn_box.button(QDialogButtonBox.Yes)
        self.btn_no = self.btn_box.button(QDialogButtonBox.No)

    def _setup_ui_modify_widgets(self):
        self.btn_yes.setObjectName("btn_red")
        self.btn_yes.setText("Oui")
        self.btn_no.setObjectName("btn_green")
        self.btn_no.setText("Non")

    def _setup_ui_create_layouts(self):
        self.layout = QVBoxLayout()

    def _setup_ui_add_widgets_to_layouts(self):
        self.layout.addWidget(self.lab_message)
        self.layout.addWidget(self.btn_box)
        self.setLayout(self.layout)

    def _setup_ui_connections(self):
        self.btn_box.accepted.connect(self.accept)
        self.btn_box.rejected.connect(self.reject)
