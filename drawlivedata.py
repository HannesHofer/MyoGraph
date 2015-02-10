# -*- coding: utf-8 -*-
import sys
import pyqtgraph as pg
from mymyo import MyMyo
from pyqtgraph.Qt import QtCore, QtGui
from PyQt4.Qt import QMutex


plotters = []
app = QtGui.QApplication([])
timer = myotimer = win = myo = None


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
        self.mutex = QMutex()

    def add_data(self, datapoint):
        self.mutex.lock()
        self._data.append(datapoint)
        if self._plotstart < self.XAXISLENGTH:
            self._data.pop(0)
        else:
            self._plotstart += 1
        self.mutex.unlock()

    def draw(self):
        self.mutex.lock()
        if not self._curve:
            self._curve = self._plot.plot(pen=self._pen)
        self._curve.setData(x=self.XAXISDATA, y=self._data[self._plotstart:])
        self.mutex.unlock()

    def addplot(self, win):
        self._plot = win.addPlot(title=self._title)
        self._plot.setRange(xRange=(0, self.XAXISLENGTH))


def update_plot_data(emgdata):
    for p, e in zip(emgdata, plotters):
        p.add_data(e)


def update_draw():
    for p in plotters:
        p.draw()


def startmyo():
    global myo
    myo = MyMyo(update_plot_data)


def main():
    global win, timer, myotimer
    win = pg.GraphicsWindow(title="Myo Sensor Data")
    win.resize(1000, 600)
    win.setBackground(None)
    pg.setConfigOptions(antialias=True)
    for i in range(8):
        if i % 2 == 0:
            win.nextRow()
        plotters.append(PlotImage(str('Sensor %s' % str(int(i) + 1))))
        plotters[i].addplot(win)

    myotimer = QtCore.QTimer()
    myotimer.timeout.connect(startmyo)
    myotimer.setSingleShot(True)
    myotimer.start(1)

    timer = QtCore.QTimer()
    timer.timeout.connect(update_draw)
    timer.start(100)


if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        main()
        QtGui.QApplication.instance().exec_()
