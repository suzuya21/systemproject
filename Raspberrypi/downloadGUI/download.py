import sys
import os
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from shadow_effect import ShadowEffect

class DownloadWidget(QWidget):
    def __init__(self):
        super(DownloadWidget, self).__init__()
        self.initUI()
        self.resize(800,480)

    def initUI(self):
        self.title = QLabel()
        self.title.setText('ダウンロード')
        self.title.setFont(QFont('メイリオ',25))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName('TitleLabel')
        self.title.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.title.setGraphicsEffect(ShadowEffect(self))

        # 科目コンボボックス
        try:
            with open('data/kamoku.csv','r',encoding='utf-8') as f:
                import csv
                reader = csv.reader(f)
                next(reader)
                kamoku = [row [0] for row in reader]
        except:
            kamoku = ['F1','F2','F3','F4','F5','M1','M2','M3','M4','M5','W2','F2','F3','F4','F5','M1','M2','M3','M4','M5','W2']
        self.kamoku = kamoku
        self.kamoku_combo = QComboBox()
        self.kamoku_combo.setFont(QFont('メイリオ',20))
        # self.kamoku_combo.setFixedSize(200,130)
        for s in self.kamoku:
            self.kamoku_combo.addItem(s)
        self.kamoku_combo.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.kamoku_combo.setGraphicsEffect(ShadowEffect(self))

        # ダウンロードボタン
        self.download_btn = QPushButton()
        self.download_btn.setText("ダウンロード")
        self.download_btn.setFont(QFont("メイリオ",15))
        self.download_btn.setObjectName('DownloadBtn')
        self.download_btn.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.download_btn.setGraphicsEffect(ShadowEffect(self))

        # レイアウト
        self.main_layout = QGridLayout()
        # self.main_layout = QVBoxLayout()
        self.head_layout = QGridLayout()
        self.middle_layout = QGridLayout()
        self.foot_layout = QGridLayout()

        self.head_layout.addWidget(QWidget(),0,0)
        self.head_layout.addWidget(self.title,0,1,1,4)
        self.head_layout.addWidget(QWidget(),0,5)
        self.middle_layout.addWidget(QWidget(),0,0)
        self.middle_layout.addWidget(self.kamoku_combo,0,1,2,1)
        self.middle_layout.addWidget(QWidget(),0,2)
        self.foot_layout.addWidget(QWidget(),0,0)
        self.foot_layout.addWidget(self.download_btn,0,1,1,2)
        self.foot_layout.addWidget(QWidget(),0,3)
        self.main_layout.addLayout(self.head_layout,0,0,3,1)
        self.main_layout.addLayout(self.middle_layout,3,0,4,1)
        self.main_layout.addLayout(self.foot_layout,8,0,2,1)
        # self.main_layout.addLayout(self.head_layout)
        # self.main_layout.addLayout(self.middle_layout)
        # self.main_layout.addLayout(self.foot_layout)
        self.main_layout.setSpacing(50)
        self.main_layout.setMargin(50)

        self.setLayout(self.main_layout)

    @Slot()
    def dwnbtn_clicked(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    print(QStyleFactory.keys())
    ex = DownloadWidget()
    try:
        with open('download.css','r',encoding='utf-8') as f:
            css = f.read()
            app.setStyleSheet(css)
    except:
        print('css open error')
    #ex = GamelikeWidget()
    ex.show()
    #reader = ICReader(ex)
    #reader.start_read()
    sys.exit(app.exec_())
