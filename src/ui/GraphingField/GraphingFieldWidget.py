from PyQt6.QtWidgets import QWidget, QVBoxLayout

from src.ui.graphingField.GraphControlToolbar import GraphControlToolbar
from src.ui.graphingField.ScatterPlotWidget import ScatterPlotWidget


class GraphingFieldWidget(QWidget):
    """
    Parent widget for graphing field
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Use vertical layout
        self.setLayout(QVBoxLayout())

        # Define toolbar and canvas
        self.toolbar = GraphControlToolbar()
        self.scatterPlot = ScatterPlotWidget(self)

        # Add widgets to layout
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.scatterPlot)
