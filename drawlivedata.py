# -*- coding: utf-8 -*-
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import sys
from random import randint

data = [[z * x for x in range(100)] for z in range(2)]
counter = 0

app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="Myo Sensor Data")
win.resize(1000, 600)
win.setBackground(None)
pg.setConfigOptions(antialias=True)
plot = ret = win.addPlot(title="Sensor1")
plot.setRange(xRange=(0, 100), yRange=(-2000, 2000))
curve = plot.plot(pen='y')
curve.setPen(color='b')


def update():
    global data, counter, curve
    data[0].pop(0)
    data[0].append(randint(0, 2000))
    counter += 1
    if counter % 10 == 0:
        curve.setData(x=data[1], y=data[0])


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)

if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()