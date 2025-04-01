from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QMainWindow,QWidget, QVBoxLayout, QFileDialog

from src.ui.ScatterPlot import ScatterPlot

class MainWindow(QMainWindow):
    fileOpenSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Set basic window attributes
        self.setWindowTitle("txtSampleView")
        self.setGeometry(0, 0, 1920, 1080)  # x, y, width, height

        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create central widget layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Creating widgets
        self.initMenuBar()
        self.plot = ScatterPlot()

        # Adding widgets into layout
        self.layout.addWidget(self.plot)

        # Signal management
        self.fileOpenSignal.connect(self.plot.updateFromFile)

    def initMenuBar(self):
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu("File")
        fopenAction = fileMenu.addAction("Open")
        fopenAction.triggered.connect(self.raiseFileOpenModal)

    @pyqtSlot(name="emitFOpen")
    def raiseFileOpenModal(self):
        file_dialog = QFileDialog(self, "Choose csv file")
        file_path, _ = file_dialog.getOpenFileName(self)

        if file_path:
            self.fileOpenSignal.emit(file_path)
