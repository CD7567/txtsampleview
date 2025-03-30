import sys
from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.main_ui import Ui_MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Ui_MainWindow()
    qMainWindow = QMainWindow()
    mainWindow.setupUi(qMainWindow)
    qMainWindow.show()
    sys.exit(app.exec())
