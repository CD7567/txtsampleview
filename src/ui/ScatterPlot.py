import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSlot

class ScatterPlot(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create graph widget
        self.plot_widget = pg.PlotWidget()

        # Create Layout
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        # Generate random data for scatter plot
        self.x_data = np.random.rand(100)
        self.y_data = np.random.rand(100)

        # Create Scatter Plot Item
        self.scatter_plot = pg.ScatterPlotItem(self.x_data, self.y_data,
                                              size=10,  # Размер точек
                                              pen=pg.mkPen(None), # Убираем обводку
                                              brush=pg.mkBrush('b')) # Заливка синим цветом

        # Add Scatter Plot Item to graph
        self.plot_widget.addItem(self.scatter_plot)

        # Configure plot axis
        self.plot_widget.setLabel('bottom', 'X Axis')
        self.plot_widget.setLabel('left', 'Y Axis')
        self.plot_widget.setTitle("Scatter Plot")

    @pyqtSlot(name="update")
    def update_data(self):
        # Update and fill with random data
        self.x_data = np.random.rand(100)
        self.y_data = np.random.rand(100)
        self.scatter_plot.setData(self.x_data, self.y_data)
