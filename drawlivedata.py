# -*- coding: utf-8 -*-
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import sys
from random import randint


plotters = []
timer = None
timer2 = None
QtGui.QApplication([])


class PlotImage:
    XAXISLENGTH = 2000
    XAXISDATA = [x for x in range(XAXISLENGTH)]

    def __init__(self, title):
        self._data = [0 for x in range(self.XAXISLENGTH)]
        self._title = title
        self._curve = None
        self._pen = pg.mkPen(color="#3366FF")
        self._plotstart = 0
        self._plot = None

    def add_data(self, datapoint):
        self._data.append(datapoint)
        self._plotstart += 1

    def draw(self):
        if not self._curve:
            self._curve = self._plot.plot(pen=self._pen)
        self._curve.setData(x=self.XAXISDATA, y=self._data[self._plotstart:])

    def addplot(self, win):
        self._plot = win.addPlot(title=self._title)
        self._plot.setRange(xRange=(0, self.XAXISLENGTH))


def update_plot_data():
    global plotters
    for p in plotters:
        p.add_data(randint(-2000, 2000))


def update_draw():
    global plotters
    for p in plotters:
        p.draw()


def update():
    update_plot_data()
    update_draw()


def main():
    win = pg.GraphicsWindow(title="Myo Sensor Data")
    win.resize(1000, 600)
    win.setBackground(None)
    pg.setConfigOptions(antialias=True)
    for i in range(8):
        if i % 2 == 0:
            win.nextRow()
        plotters.append(PlotImage(str('Sensor %s' % str(int(i)+1))))
        plotters[i].addplot(win)

timer = QtCore.QTimer()
timer.timeout.connect(update_plot_data)
timer.start(10)

timer2 = QtCore.QTimer()
timer2.timeout.connect(update_draw)
timer2.start(100)

if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        main()
        QtGui.QApplication.instance().exec_()