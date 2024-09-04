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
            
            #btn_red {
                background-color: #f44336;
                color: white;
                font-size: 14px;
            }
            
            #btn_green {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
            }
            
            #btn_red:hover {
                background-color: red;
            }
            
            #btn_green:hover {
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
        self.btn_yes.setObjectName("btn_red")
        self.btn_yes.setText("Oui")
        self.btn_no.setObjectName("btn_green")
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
