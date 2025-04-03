import numpy as np
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QDockWidget

from src.ui.BottomDock.PointTableWidget import PointTableWidget


class BottomDock(QDockWidget):
    def __init__(self):
        super().__init__()

        self.setVisible(False)
        self.setWindowTitle("Selection")
        self.tableWidget = PointTableWidget()
        self.setWidget(self.tableWidget)

    @pyqtSlot(bool)
    def slotVisible(self, isVisible: bool):
        self.setVisible(isVisible)

    @pyqtSlot(np.ndarray, list)
    def slotSelect(self, data: np.ndarray, headers: list):
        self.tableWidget.updateModel(data, headers)
