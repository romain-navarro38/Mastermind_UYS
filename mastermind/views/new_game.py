from PySide6.QtWidgets import QLabel, QComboBox, QPushButton, QGridLayout, QDialog, QWidget

from mastermind.utils.parameters import Level, Try


class NewGame(QDialog):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setWindowTitle("Nouvelle partie")
        self.setup_ui()
        self.setStyleSheet("""
            QComboBox {
                border: 1px solid gray;
                border-radius: 3px;
                padding: 1px 18px 1px 10px;
                min-width: 6em;
                background-color: yellow;
            }
            
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid; /* just a single line */
                border-top-right-radius: 3px; /* same radius as the QComboBox */
                border-bottom-right-radius: 3px;
            }
            
            QComboBox::down-arrow:on { /* shift the arrow when popup is open */
                top: 1px;
                left: 1px;
            }
            
            QAbstractItemView {
                border: 2px solid darkgray;
                selection-background-color: lightgray;
                background-color: yellow;
                color: black;
            }
            
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

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.la_description_level = QLabel("Nombre de couleurs disponibles : ")
        self.la_description_try = QLabel("Nombre de tentatives maximum : ")
        self.cb_level = QComboBox()
        self.cb_try = QComboBox()
        self.btn_exec = QPushButton("Lancer")

    def modify_widgets(self):
        for level in Level:
            self.cb_level.addItem(f"{level} - {level.value} couleurs", level)
        for tries in Try:
            self.cb_try.addItem(f"{tries} - {tries.value} essais", tries)

        self.btn_exec.setObjectName("btn_green")

    def create_layouts(self):
        self.main_layout = QGridLayout(self)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.la_description_level, 0, 0, 1, 1)
        self.main_layout.addWidget(self.cb_level, 0, 1, 1, 1)
        self.main_layout.addWidget(self.la_description_try, 1, 0, 1, 1)
        self.main_layout.addWidget(self.cb_try, 1, 1, 1, 1)
        self.main_layout.addWidget(self.btn_exec, 2, 0, 1, 2)

    def setup_connections(self):
        self.btn_exec.clicked.connect(self.accept)

    def get_params_new_game(self):
        return self.cb_level.currentData(), self.cb_try.currentData()


if __name__ == '__main__':
    from sys import exit
    from PySide6.QtWidgets import QApplication

    app = QApplication()
    window = NewGame()
    window.show()
    exit(app.exec())
