from PyQt5.QtWidgets import QApplication
from appfunctionality import AppCore

class MainApp(AppCore):
    def __init__(self):
        super().__init__()



if __name__ == "__main__":

    """ Application layout and the functionality is inherited """

    app = QApplication([])
    photo_editor = MainApp()
    photo_editor.show()
    app.exec_()