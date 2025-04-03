import numpy as np
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QDockWidget

from src.ui.SelectionDock.PointTableWidget import PointTableWidget


class SelectionDock(QDockWidget):
    def __init__(self):
        super().__init__()

        self.setVisible(False)
        self.setWindowTitle("Selection")
        self.tableWidget = PointTableWidget()
        self.setWidget(self.tableWidget)

    @pyqtSlot(bool)
    def slotVisible(self, isVisible: bool):
        self.setVisible(isVisible)

    @pyqtSlot(np.ndarray)
    def slotSelect(self, data: np.ndarray):
        self.tableWidget.updateModel(data)
