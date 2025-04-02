from itertools import cycle

import pyqtgraph as pg
import pandas as pd
from PyQt6.QtCore import pyqtSlot
from pyqtgraph import PlotWidget


class ScatterPlotWidget(PlotWidget):
    """
    Graphing canvas
    """

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
