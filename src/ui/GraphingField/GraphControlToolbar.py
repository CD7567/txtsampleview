import qtawesome as qta
from PyQt6.QtWidgets import QToolBar, QPushButton, QButtonGroup


class GraphControlToolbar(QToolBar):
    """
    Toolbar widget for graphing field
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Button to enable scrolling behaviour
        self.scrollMoveButton = QPushButton(qta.icon("mdi6.cursor-move"), None)
        self.scrollMoveButton.setCheckable(True)
        self.scrollMoveButton.setChecked(True)
        self.scrollMoveButton.setToolTip("Scroll through graph")

        # Button to enable selection behaviour
        self.scrollSelectButton = QPushButton(qta.icon("mdi6.select-drag"), None)
        self.scrollSelectButton.setCheckable(True)
        self.scrollSelectButton.setChecked(False)
        self.scrollSelectButton.setToolTip("Select points in rectangle")

        # Button group to make selection exclusive
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.setExclusive(True)
        self.buttonGroup.addButton(self.scrollMoveButton)
        self.buttonGroup.addButton(self.scrollSelectButton)

        # Add widgets into layout
        self.addWidget(self.scrollMoveButton)
        self.addWidget(self.scrollSelectButton)
