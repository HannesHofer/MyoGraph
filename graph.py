# -*- coding: utf-8 -*-
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import sys


app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="Myo Sensor Data")
win.resize(1000, 600)
win.setBackground(None)

pg.setConfigOptions(antialias=True)
p = []
curve = []
for i in range(8):
    if i % 2 == 0:
        win.nextRow()
    _title = "Sensor %s " % str(int(i) + 1)
    ret = win.addPlot(title=_title)
    p.append(ret)
    p[i].setRange(xRange=(0, 200), yRange=(-4, 4))
    # p[i].disableAutoRange(axis='x')
    curve.append(p[i].plot(pen='y'))
    curve[i].setPen(color='r')

data = np.random.normal(size=(10, 1000))
ptr = 0


def update():
    global curve, data, ptr, p
    for u in range(len(p)):
        curve[u].setData(data[ptr % 10])
        ptr += 1


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(200)

if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
