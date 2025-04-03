from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt


class PointTableDataModel(QAbstractTableModel):
    def __init__(self, data, headers, parent=None):
        super().__init__(parent)

        self.data = data
        self.headers = headers

    def rowCount(self, parent=QModelIndex()):
        return len(self.data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        if role == Qt.DisplayRole:
            return str(self.data[self.headers[col]][row])

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return None

    def updateData(self, data):
        self.beginResetModel()
        self.data = data
        self.endResetModel()
