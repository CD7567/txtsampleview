import pyqtgraph as pg
import pandas as pd
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSlot

class ScatterPlot(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create graph widget
        self.x = []
        self.y = []
        self.data = []
        self.plot_widget = pg.PlotWidget()

        # Create Layout
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        # Create Scatter Plot Item
        self.scatter_plot = pg.ScatterPlotItem(x=self.x, y=self.y, data=self.data,
                                               size=10,
                                               pen=pg.mkPen(None),
                                               brush=pg.mkBrush('b'),
                                               hoverable=True)

        # Add Scatter Plot Item to graph
        self.plot_widget.addItem(self.scatter_plot)

        # Configure plot axis
        self.plot_widget.setLabel('bottom', 'X Axis')
        self.plot_widget.setLabel('left', 'Y Axis')

    @pyqtSlot(str, name="csvUpdate")
    def updateFromFile(self, filename):
        # Update with data from csv
        csv = pd.read_csv(filename, index_col=False)
        self.x = csv['x']
        self.y = csv['y']
        self.data = csv['label']
        self.scatter_plot.setData(x=self.x, y=self.y, data=self.data)
