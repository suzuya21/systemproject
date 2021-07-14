from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from shadow_effect import ShadowEffect

# 出席,遅刻,欠席とか出欠状況が表示されるラベル
class SyussekiWidget(QLabel):
    def __init__(self):
        super(SyussekiWidget, self).__init__()
        self.attend = "出席"
        self.late = "遅刻"
        self.absence = "欠席"
        self.initUI()

    def initUI(self):
        self.setFont(QFont('メイリオ', 30))
        self.setAlignment(Qt.AlignCenter)
        # self.syusseki_label.setStyleSheet("border-radius:50px;color:#F2B33D;background-color: white;border-color:#F2B33D;border-width:4px;border-style:solid;")
        # self.setStyleSheet("border-radius:40%;color:#F2B33D;background-color: white;")
        # self.setGraphicsEffect(ShadowEffect(self).set_shadow_color(184, 136, 59, 180))
        self.setMargin(20)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def setText(self, text:str) -> None:
        super(SyussekiWidget, self).setText(text)
        self.change_color(text)

    def change_color(self,text:str):
        if text == self.absence:
            self.setStyleSheet("border-radius:40%;color:#b22222;background-color:#ffb6c1;")
            self.setGraphicsEffect(ShadowEffect(self).set_shadow_color(64, 64, 64, 180))
        elif text == self.late:
            self.setStyleSheet("border-radius:40%;color:#F2B33D;background-color: white;")
            self.setGraphicsEffect(ShadowEffect(self).set_shadow_color(184, 136, 59, 180))
        else:
            self.setStyleSheet("border-radius:40%;color:#8AC75A;background-color: white;")
            self.setGraphicsEffect(ShadowEffect(self).set_shadow_color(64, 64, 64, 180))

