#!/usr/bin/python3
"""
Plots channels zero and one in two different windows. Requires pyqtgraph.
"""

import sys

import numpy as np
import pyqtgraph as pg
import scipy.signal as signal
from PyQt5 import QtCore, QtGui
from pyfirmata2 import Arduino

import IIRFilter as IIR

PORT = Arduino.AUTODETECT

# create a global QT application object
app = QtGui.QApplication(sys.argv)

# signals to all threads in endless loops that we'd like to run these
running = True


class QtPanningPlot:
    def __init__(self, title):
        self.win = pg.GraphicsLayoutWidget()
        self.win.setWindowTitle(title)
        self.plt = self.win.addPlot()
        self.plt.setYRange(-1, 1)
        self.plt.setXRange(0, 45)
        self.curve = self.plt.plot()
        self.data = []
        # any additional initalisation code goes here (filters etc)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)
        self.layout = QtGui.QGridLayout()
        self.win.setLayout(self.layout)
        self.win.show()

    def update(self):
        self.data = self.data[-45:]
        if self.data:
            self.curve.setData(np.hstack(self.data))

    def addData(self, d):
        self.data.append(d)


# Let's create two instances of plot windows
qtPanningPlot1 = QtPanningPlot("VCO output - unfiltered")
qtPanningPlot2 = QtPanningPlot("VCO output - filtered")

# sampling rate: 100Hz
samplingRate = 100

cutoff_list = [24, 45]

for i in range(len(cutoff_list)):
    cutoff_list[i] = cutoff_list[i] / samplingRate * 2

coeff = signal.butter(2, cutoff_list, 'bandpass', output='sos')

Filter = IIR.IIRFilter(coeff)


# called for every new sample at channel 0 which has arrived from the Arduino
# "data" contains the new sample
def callBack(data):
    # filter your channel 0 samples here:
    # data = self.filter_of_channel0.dofilter(data)
    # send the sample to the plotwindow
    qtPanningPlot1.addData(data)
    filtered_data = Filter.filter(data)
    qtPanningPlot2.addData(filtered_data)


# Get the Arduino board.
board = Arduino(PORT)

# Set the sampling rate in the Arduino
board.samplingOn(1000 / samplingRate)

# Register the callback which adds the data to the animated plot
# The function "callback" (see above) is called when data has
# arrived on channel 0.

board.analog[0].register_callback(callBack)

# Enable the callback
board.analog[0].enable_reporting()

# showing all the windows
app.exec_()

# needs to be called to close the serial port
board.exit()

print("Finished")
