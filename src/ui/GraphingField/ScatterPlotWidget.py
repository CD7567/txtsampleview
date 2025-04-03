from itertools import cycle

import pandas as pd
import pyqtgraph as pg
from PyQt6.QtCore import pyqtSlot
from pyqtgraph import PlotWidget


class ScatterPlotWidget(PlotWidget):
    """
    Graphing canvas
    """

    scrollEnabled = True
    drawRoiRect = False
    initialMousePos = None
    roiRect = None

    def __init__(self, parent=None):
        super().__init__(parent)

        # Configure colormap for points
        self.colormap = [
            '#66B2FF',
            '#FF6666',
            '#66FF66',
            '#FFCC66',
            '#CC99FF',
            '#66FFFF',
            '#FFB266',
            '#A6B2FF',
            '#B2B2B2',
            '#FF8533',
            '#77B5FE',
            '#F08080',
            '#90EE90',
            '#F4A460',
            '#DDA0DD',
            '#AFEEEE',
            '#F0E68C',
            '#D3D3D3',
            '#ADD8E6',
            '#98FB98',
        ]

        # Configure plot axis
        self.setLabel('bottom', 'X Axis')
        self.setLabel('left', 'Y Axis')
        self.autoRange()

    def mousePressEvent(self, event):
        if self.scrollEnabled:
            super().mousePressEvent(event)
            return

        self.resetRoiRect()
        self.drawRoiRect = True
        self.initialMousePos = self.plotItem.vb.mapSceneToView(event.position())

    def mouseReleaseEvent(self, event):
        if self.scrollEnabled:
            super().mouseReleaseEvent(event)
            return

        self.drawRoiRect = False
        self.plotItem

    def mouseMoveEvent(self, event):
        if self.scrollEnabled:
            super().mouseMoveEvent(event)
            return

        if self.initialMousePos is None or not self.drawRoiRect:
            return

        mousePos = self.plotItem.vb.mapSceneToView(event.position())
        bottomLeft = [min(self.initialMousePos.x(), mousePos.x()), min(self.initialMousePos.y(), mousePos.y())]
        topRight = [max(self.initialMousePos.x(), mousePos.x()), max(self.initialMousePos.y(), mousePos.y())]
        self.roiRect.setPos(bottomLeft)
        self.roiRect.setSize([topRight[0] - bottomLeft[0], topRight[1] - bottomLeft[1]])

    def resetRoiRect(self):
        if self.roiRect in self.items():
            self.removeItem(self.roiRect)

        self.initialMousePos = None

        self.roiRect = pg.RectROI(
            pos=[-1, -1],
            size=[0, 0],
            rotatable=False,
            invertible=True,
            pen=pg.mkPen([200, 200, 200], width=2, style=pg.QtCore.Qt.PenStyle.DotLine),
            hoverPen=pg.mkPen([255, 255, 255], width=2, style=pg.QtCore.Qt.PenStyle.DashLine)
        )

        self.addItem(self.roiRect)
        self.roiRect.setZValue(1000)

    @pyqtSlot()
    def activateMoveTool(self):
        self.scrollEnabled = True

    @pyqtSlot()
    def activateSelectTool(self):
        self.scrollEnabled = False

    @pyqtSlot(str, name="csvUpdate")
    def updateFromFile(self, filename):
        # Update with data from csv
        csv = pd.read_csv(filename, index_col=False)
        colorIt = cycle(self.colormap)

        self.clear()

        if 'label' in csv.columns:
            grouped = csv.groupby('label')

            for label, group in grouped:
                scatter = pg.ScatterPlotItem(
                    x=group['x'],
                    y=group['y'],
                    data=group.apply(lambda row: "[{}] {}".format(row['label'], row['data']), axis=1),
                    size=10,
                    pen=pg.mkPen(None),
                    brush=pg.mkBrush(next(colorIt)),
                    hoverable=True
                )
                self.addItem(scatter)
        else:
            scatter = pg.ScatterPlotItem(
                x=csv['x'],
                y=csv['y'],
                data=csv['data'],
                size=10,
                pen=pg.mkPen(None),
                brush=pg.mkBrush(next(colorIt)),
                hoverable=True
            )
            self.addItem(scatter)
