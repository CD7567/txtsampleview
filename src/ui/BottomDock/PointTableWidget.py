import numpy as np
from PyQt6.QtWidgets import QTableView, QHeaderView

from src.ui.BottomDock.PointTableDataModel import PointTableDataModel


class PointTableWidget(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setEditTriggers(QTableView.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.model = None
        self.headers = None

    def updateModel(self, data: np.ndarray, headers: list):
        self.model = PointTableDataModel(data, headers)
        self.setModel(self.model)
