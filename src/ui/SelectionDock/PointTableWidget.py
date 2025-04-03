import numpy as np
from PyQt6.QtWidgets import QTableView, QHeaderView

from src.ui.SelectionDock.PointTableDataModel import PointTableDataModel


class PointTableWidget(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setEditTriggers(QTableView.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def updateModel(self, data: np.ndarray):
        self.setModel(PointTableDataModel(data))
