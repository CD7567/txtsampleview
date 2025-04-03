import qtawesome as qta
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFileDialog

from src.ui.BottomDock.BottomDock import BottomDock
from src.ui.GraphingField.GraphingFieldWidget import GraphingFieldWidget


class MainWindow(QMainWindow):
    fileOpenSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Set basic window attributes
        self.setWindowTitle("txtSampleView")
        self.setGeometry(0, 0, 1920, 1080)

        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.dock = BottomDock()

        # Create central widget layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Create widgets
        self.initMenuBar()
        self.plot = GraphingFieldWidget()
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.dock)

        # Add widgets into layout
        self.layout.addWidget(self.plot)

        # Signal management
        self.fileOpenSignal.connect(self.plot.scatterPlot.updateFromFile)
        self.plot.scatterPlot.sigDockControl.connect(self.dock.slotVisible)
        self.plot.scatterPlot.sigItemsSelected.connect(self.dock.slotSelect)

    def initMenuBar(self):
        """
        Initialize menu bar
        """

        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu("File")
        fopenAction = fileMenu.addAction(qta.icon("mdi6.folder"), "Load CSV")
        fopenAction.triggered.connect(self.raiseFileOpenModal)

    @pyqtSlot(name="emitFOpen")
    def raiseFileOpenModal(self):
        file_dialog = QFileDialog(self, "Choose csv file")
        file_path, _ = file_dialog.getOpenFileName(self)

        if file_path:
            self.fileOpenSignal.emit(file_path)
