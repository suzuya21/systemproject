from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import datetime
from shadow_effect import ShadowEffect

class ClockWidget(QLabel):
    def __init__(self,fontsize=30,height=100,width=300):
        super(ClockWidget, self).__init__()
        self.fontsize = fontsize
        self._height = height
        self._width = width
        self.interval = 1000/5 # ms
        self.timer = QTimer()
        self.timer.setInterval(self.interval)
        self.timer.timeout.connect(self.update_time)
        self.timerco = 0
        self.initUI()

    def start(self):
        self.timer.start()

    def initUI(self):
        self.setAlignment(Qt.AlignCenter)
        # self.setFixedSize(self._width,self._height)
        # self.label = QLabel(self)
        self.setFont(QFont('メイリオ',self.fontsize))
        self.setObjectName('ClockWidget')
        self.setGraphicsEffect(ShadowEffect(self))
        self.update_time()

    @Slot()
    def update_time(self):
        now = datetime.datetime.now().time()
        if self.timerco % 5 <= 2:
            # self.setText('<font color=\"black\">'+str(now.hour).zfill(2)+'</font><font color=\"black\">:</font>'+str(now.minute).zfill(2)+'</font><font color=\"black\">:</font>'+str(now.second).zfill(2))
            self.setText('<font color=\"black\">'+str(now.hour).zfill(2)+'</font><font color=\"black\">:</font>'+str(now.minute).zfill(2)+'</font>')
        elif self.timerco % 5 == 5:
            # self.setText('<font color=\"black\">'+str(now.hour).zfill(2)+'</font><font color=\"gray\">:</font>'+str(now.minute).zfill(2)+':'+str(now.second).zfill(2))
            self.setText('<font color=\"black\">'+str(now.hour).zfill(2)+'</font><font color=\"gray\">:</font>'+str(now.minute).zfill(2)+'</font>')
        else:
            # self.setText('<font color=\"black\">'+str(now.hour).zfill(2)+'</font><font color=\"white\">:</font>'+str(now.minute).zfill(2)+'</font><font color=\"white\">:</font>'+str(now.second).zfill(2))
            self.setText('<font color=\"black\">'+str(now.hour).zfill(2)+'</font><font color=\"white\">:</font>'+str(now.minute).zfill(2)+'</font>')
        self.timerco += 1
