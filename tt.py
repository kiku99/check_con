import pyqtgraph as pg

from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, Qt, QThread, QTimer

import random


class ExMain(QWidget):
    def __init__(self):
        super().__init__()

        self.current_data = 100
        self.top=0
        hbox = QHBoxLayout()
        self.pw1 = pg.PlotWidget(title="a")

        hbox.addWidget(self.pw1)
        self.setLayout(hbox)

        self.setWindowTitle("pyqtgraph 예제 - realtime")

        self.x = [1]
        self.y = [100]
        self.data=[60, 60, 60,150,120,120,390,600,480,210,210,210,60,60,90,180,240,480,270,240,60,60,180,210,270,420,330,240,330,660,
                  120,240,450,5130,1170,240,510,1110,750,240,150,210,2130,300, 390,1500,480,7770,210,480,300,540,5670,
                  480,420,390,450,960,660,1650,630,930,360,480,570,270,210,240,90,120,60,120,120,150,60]
        self.pl = self.pw1.plot(pen='g')

        self.mytimer = QTimer()
        self.mytimer.start(1000)  # 1초마다 차트 갱신 위함...
        self.mytimer.timeout.connect(self.get_data)

        self.draw_chart(self.x, self.y)
        self.show()

    def draw_chart(self, x, y):
        self.pl.setData(x=x, y=y,)  # line chart 그리기

    @pyqtSlot()
    def get_data(self):

        last_x = self.x[self.top]
        self.top+=1
        self.x.append(last_x + 1)

        if(len(self.data)<=self.top):
            self.y.append(random.random()*10+90)
        else:
            self.y.append(100-self.data[self.top]*0.005)
        self.draw_chart(self.x, self.y)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    ex = ExMain()

    sys.exit(app.exec_())