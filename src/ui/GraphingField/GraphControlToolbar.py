import qtawesome as qta
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QToolBar, QPushButton, QButtonGroup


class GraphControlToolbar(QToolBar):
    """
    Toolbar widget for graphing field
    """

    moveToolToggledOn = pyqtSignal()
    selectToolToggledOn = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Button to enable moving behaviour
        self.moveToggleButton = QPushButton(qta.icon("mdi6.cursor-move"), None)
        self.moveToggleButton.setCheckable(True)
        self.moveToggleButton.setChecked(True)
        self.moveToggleButton.setToolTip("Scroll through graph")

        # Button to enable selection behaviour
        self.selectToggleButton = QPushButton(qta.icon("mdi6.select-drag"), None)
        self.selectToggleButton.setCheckable(True)
        self.selectToggleButton.setChecked(False)
        self.selectToggleButton.setToolTip("Select points in rectangle")

        # Button group to make selection exclusive
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.setExclusive(True)
        self.buttonGroup.addButton(self.moveToggleButton)
        self.buttonGroup.addButton(self.selectToggleButton)

        # Add widgets into layout
        self.addWidget(self.moveToggleButton)
        self.addWidget(self.selectToggleButton)

        # Manage signals
        self.buttonGroup.buttonToggled.connect(self.buttonToggled)

    def buttonToggled(self, button: QPushButton, checked: bool):
        if checked:
            if button is self.moveToggleButton:
                self.moveToolToggledOn.emit()
            elif button is self.selectToggleButton:
                self.selectToolToggledOn.emit()
