import sys
from PyQt6.QtWidgets import QMainWindow,QWidget, QVBoxLayout, QPushButton

from src.ui.ScatterPlot import ScatterPlot

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set basic window attributes
        self.setWindowTitle("txtSampleView")
        self.setGeometry(100, 100, 600, 400)  # x, y, width, height

        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create central widget layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Creating widgets
        self.button = QPushButton("Push me")
        self.plot = ScatterPlot()

        # Adding widgets into layout
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.plot)

        # Signal management
        self.button.clicked.connect(self.plot.update)
