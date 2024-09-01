from PySide6.QtWidgets import QWidget, QDialog, QLabel, QDialogButtonBox, QVBoxLayout


class ConfirmationMessage(QDialog):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setWindowTitle("Confirmation")
        self.setup_ui()
        self.setStyleSheet("""
            QDialog {
                background-color: blue;
            }
            QLabel {
                background-color: blue;
                color: white;
            }
            #btn_yes {
                background-color: #F57C72; /* Red */
                color: white;
                font-size: 12px;
            }
            #btn_no {
                background-color: #86CC89; /* Green */
                color: white;
                font-size: 12px;
                font-weight: bold;
            }
            #btn_yes:focus {
                background-color: red;
            }
            #btn_no:focus {
                background-color: green;
            }
            #btn_yes:hover {
                background-color: red;
            }
            #btn_no:hover {
                background-color: green;
            }
        """)
        self.btn_no.setFocus()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.lab_message = QLabel("Une partie est en cours !\nVoulez-vous vraiment l'arrêter ?")
        self.btn_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        self.btn_yes = self.btn_box.button(QDialogButtonBox.Yes)
        self.btn_no = self.btn_box.button(QDialogButtonBox.No)

    def modify_widgets(self):
        self.btn_yes.setObjectName("btn_yes")
        self.btn_yes.setText("Oui")
        self.btn_no.setObjectName("btn_no")
        self.btn_no.setText("Non")

    def create_layouts(self):
        self.layout = QVBoxLayout()

    def add_widgets_to_layouts(self):
        self.layout.addWidget(self.lab_message)
        self.layout.addWidget(self.btn_box)
        self.setLayout(self.layout)

    def setup_connections(self):
        self.btn_box.accepted.connect(self.accept)
        self.btn_box.rejected.connect(self.reject)
