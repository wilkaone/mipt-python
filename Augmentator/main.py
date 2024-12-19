import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from ui.interface import Ui_MainWindow
from tools.handler_events import HandlerEvents

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.handler_events = HandlerEvents(self, self.ui)
        self.data_for_aug = dict()
        self.data_for_show = dict()
        
        self.connect_buttons()
        self.handler_events.signal_message.connect(self.send_message)
        self.ui.combobox_classes.currentTextChanged.connect(self.change_class)

    def connect_buttons(self):
        self.ui.button_load_dataset.clicked.connect(self.load_dataset)
        self.ui.button_show_dataset.clicked.connect(self.show_dataset)
        self.ui.button_augment_dataset.clicked.connect(self.augment_dataset)
        self.ui.button_back.clicked.connect(self.back_image)
        self.ui.button_next.clicked.connect(self.next_image)

    def load_dataset(self):
        self.data_for_aug = self.handler_events.load_dataset()

    def show_dataset(self):
        self.data_for_show = self.handler_events.show_dataset()

    def back_image(self):
        self.handler_events.back_image(self.data_for_show)

    def next_image(self):
        self.handler_events.next_image(self.data_for_show)

    def change_class(self, text):
        print(text)
        self.handler_events.change_class(text, self.data_for_show);

    def augment_dataset(self):
        if len(self.data_for_aug) <= 0:
            return
        else:
            self.handler_events.augment_dataset(self.data_for_aug)

    def send_message(self, str):
        print(str)
        msg = QMessageBox()
        msg.setWindowTitle("Info")
        msg.setText(str)
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        result = msg.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

