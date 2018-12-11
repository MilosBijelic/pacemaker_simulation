import numpy as np
import random as rd

from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QApplication, QStyleFactory

class CustomFigCanvas(FigureCanvas, TimedAnimation):

    def __init__(self, xlim, ylim, width, height, resolution):

        self.data1 = []
        self.data2 = []

        # the data
        self.xlim = 200
        self.n = np.linspace(0, self.xlim - 1, self.xlim)
        self.y1 = self.n * 0.0
        self.y2 = self.n * 0.0

        # the window
        self.fig = Figure(figsize=(width,height), dpi=resolution)
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)

        # Plot 1 settings
        self.line1 = Line2D([], [], color='blue')
        self.ax1.add_line(self.line1)
        self.ax1.set_xlim(xlim[0], xlim[1])
        self.ax1.set_ylim(ylim[0], ylim[1])
        self.ax1.set_title("Atrial")
        self.ax1.set_xlabel("Time")
        self.ax1.set_ylabel("Voltage (V)")
        
        self.line2 = Line2D([], [], color='red')
        self.ax2.add_line(self.line2)
        self.ax2.set_xlim(xlim[0], xlim[1])
        self.ax2.set_ylim(ylim[0], ylim[1])
        self.ax2.set_title("Ventricular")
        self.ax2.set_xlabel("Time")
        self.ax2.set_ylabel("Voltage (V)")

        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval = 50, blit = True)

    def new_frame_seq(self):
        return iter(range(self.n.size))

    def _init_draw(self):
        self.line1.set_data([],[])
        self.line2.set_data([],[])
    
    def add_data(self, val1,val2):
        self.data1.append(val1)
        self.data2.append(val2)

    def _step(self, *args):
        try:
            TimedAnimation._step(self, *args)
        except Exception as e:
            self.abc += 1
            print(str(self.abc))
            TimedAnimation._stop(self)
            pass

    def _draw_frame(self, framedata):
        margin = 2
        while(len(self.data1) > 0 and len(self.data2) > 0):

            # scroll data
            self.y1 = np.roll(self.y1, -1)
            self.y1[-1] = self.data1[0]

            
            self.y2 = np.roll(self.y2, -1)
            self.y2[-1] = self.data2[0]
            

            del(self.data1[0])
            del(self.data2[0])
            
        self.line1.set_data(self.n[ 0 : self.n.size - margin ], self.y1[ 0 : self.n.size - margin ])
        self.line2.set_data(self.n[ 0 : self.n.size - margin ], self.y2[ 0 : self.n.size - margin ])
        self._drawn_artists = [self.line1, self.line2]

