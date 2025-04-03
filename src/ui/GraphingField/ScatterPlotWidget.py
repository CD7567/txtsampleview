from itertools import cycle

import numpy as np
import pandas as pd
import pyqtgraph as pg
from PyQt6.QtCore import pyqtSlot, pyqtSignal, Qt
from pyqtgraph import PlotWidget


class ScatterPlotWidget(PlotWidget):
    """
    Graphing canvas
    """

    scrollEnabled = True
    drawRoiRect = False
    displayLabel = False

    initialMousePos = None
    roiRect = None
    scatterItem = None

    dtypeWithLabel = [("x", "<f8"), ("y", "f8"), ("label", "O"), ("data", "O")]
    dtypeWithoutLabel = [("x", "<f8"), ("y", "f8"), ("data", "O")]

    sigDockControl = pyqtSignal(bool)
    sigItemsSelected = pyqtSignal(np.ndarray)

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

        if event.button() == Qt.LeftButton:
            self.drawRoiRect = True
            self.initialMousePos = self.plotItem.vb.mapSceneToView(event.position())
            self.roiRect.setPos([self.initialMousePos.x(), self.initialMousePos.y()])
            self.roiRect.setSize([0, 0])
            self.addItem(self.roiRect)

    def mouseReleaseEvent(self, event):
        if self.scrollEnabled:
            super().mouseReleaseEvent(event)
            return

        self.drawRoiRect = False

        roiPos = self.roiRect.pos()
        roiSize = self.roiRect.size()

        if self.scatterItem is None:
            return

        selected = self.scatterItem.data[
            (self.scatterItem.data['x'] >= roiPos[0]) &
            (self.scatterItem.data['x'] <= roiPos[0] + roiSize[0]) &
            (self.scatterItem.data['y'] >= roiPos[1]) &
            (self.scatterItem.data['y'] <= roiPos[1] + roiSize[1])
            ]

        if self.displayLabel:
            formatted = np.zeros(len(selected), dtype=self.dtypeWithLabel)

            formatted["x"] = selected["x"]
            formatted["y"] = selected["y"]

            for idx, piece in enumerate(selected["data"]):
                formatted["label"][idx] = piece[0]
                formatted["data"][idx] = piece[1]

            self.sigItemsSelected.emit(formatted)
        else:
            formatted = np.zeros(len(selected), dtype=self.dtypeWithoutLabel)

            formatted["x"] = selected["x"]
            formatted["y"] = selected["y"]
            formatted["data"] = selected["data"]

            self.sigItemsSelected.emit(formatted)

        self.sigDockControl.emit(True)

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
        if self.roiRect is None:
            self.roiRect = pg.RectROI(
                pos=[0, 0],
                size=[0, 0],
                rotatable=False,
                invertible=True,
                pen=pg.mkPen([200, 200, 200], width=2, style=pg.QtCore.Qt.PenStyle.DotLine),
                hoverPen=pg.mkPen([255, 255, 255], width=2, style=pg.QtCore.Qt.PenStyle.DashLine)
            )

            self.roiRect.setZValue(1000)
        elif self.roiRect in self.items():
            self.removeItem(self.roiRect)

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
        self.sigDockControl.emit(False)

        if 'label' in csv.columns:
            grouped = csv.groupby('label')

            self.displayLabel = True

            for label, group in grouped:
                self.scatterItem = pg.ScatterPlotItem(
                    x=group["x"],
                    y=group["y"],
                    data=group.apply(lambda row: (row['label'], row['data']), axis=1),
                    size=10,
                    pen=pg.mkPen(None),
                    brush=pg.mkBrush(next(colorIt)),
                    hoverable=True
                )

            self.sigItemsSelected.emit(np.ndarray(0, dtype=self.dtypeWithLabel))
        else:
            self.scatterItem = pg.ScatterPlotItem(
                x=csv["x"],
                y=csv["y"],
                data=csv["data"],
                size=10,
                pen=pg.mkPen(None),
                brush=pg.mkBrush(next(colorIt)),
                hoverable=True
            )

            self.sigItemsSelected.emit(np.ndarray(0, dtype=self.dtypeWithoutLabel))

        self.addItem(self.scatterItem)
