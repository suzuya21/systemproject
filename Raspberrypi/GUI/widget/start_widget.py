"""
出席管理スタート画面
"""
import os.path

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from shadow_effect import ShadowEffect

# 科目と回数を選択する画面 attendance_manegement_gui.pyを実行して最初に表示される
class StartWidget(QWidget):
    clicked_signal = Signal(str,str)
    def __init__(self):
        super(StartWidget, self).__init__()
        self.initUI()
        self.initSlot()

    def initUI(self):
        # タイトル
        self.title_label = QLabel("<html>出席管理 <img src='images/fileio2.png'></html>")
        self.title_label.setFont(QFont('メイリオ',30))
        self.title_label.setAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        self.title_label.setObjectName('TitleLabel')
        self.title_label.setGraphicsEffect(ShadowEffect(self))
        self.title_label.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)

        # 科目コンボボックス
        try:
            with open(os.path.abspath(f'kamoku.csv'), 'r', encoding='utf-8') as f:
                import csv
                reader = csv.reader(f)
                next(reader)
                kamoku = [row [0] for row in reader]
        except:
            import traceback
            traceback.print_exc()
            kamoku = ['F1', 'F2', 'F3', 'F4_1', 'F4_2', 'M1', 'M2', 'M3', 'M4', 'T2', 'T3_1', 'T3_2', 'T4', 'T5', 'Th2', 'Th34',
         'Th5_1', 'Th5_2', 'W12', 'W3_1', 'W3_2', 'W4', 'W5_1', 'W5_2']
        self.kamoku = kamoku
        self.kamoku_combo = QComboBox()
        self.kamoku_combo.setFont(QFont('メイリオ',20))
        # self.kamoku_combo.setFixedSize(200,130)
        for s in self.kamoku:
            self.kamoku_combo.addItem(s)
        self.kamoku_combo.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.kamoku_combo.setGraphicsEffect(ShadowEffect(self))

        # 回数コンボボックス
        self.kaisu = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        self.kaisu_combo = QComboBox()
        self.kaisu_combo.setFont(QFont('メイリオ',20))
        # self.kaisu_combo.setFixedSize(200,130)
        for i,s in enumerate(self.kaisu):
            self.kaisu_combo.addItem(str(s))
        self.kaisu_combo.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.kaisu_combo.setGraphicsEffect(ShadowEffect(self))
        self.kaisu_combo.setWindowIcon(QIcon(QPixmap('../images/return.png')))

        # スタートボタン
        self.start_btn = QPushButton()
        self.start_btn.setText("開始")
        self.start_btn.setFont(QFont("メイリオ",30))
        self.start_btn.setObjectName('StartBtn')
        self.start_btn.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.start_btn.setGraphicsEffect(ShadowEffect(self))

        # レイアウト
        self.main_layout = QVBoxLayout()
        self.main_layout = QGridLayout()
        self.top_layout = QGridLayout()
        self.middle_layout = QGridLayout()
        self.bottom_layout = QGridLayout()
        self.main_layout.setMargin(50)
        self.main_layout.setSpacing(50)
        # self.main_layout.setContentsMargins(0,25,0,25)
        self.top_layout.addWidget(QWidget(),0,0)
        self.top_layout.addWidget(self.title_label,0,1,1,3)
        self.top_layout.addWidget(QWidget(),0,4)

        self.middle_layout.addWidget(self.kamoku_combo,0,0,1,2)
        self.middle_layout.addWidget(QWidget(),0,2)
        self.middle_layout.addWidget(self.kaisu_combo,0,3,1,2)
        self.bottom_layout.addWidget(QWidget(),0,0)
        self.bottom_layout.addWidget(self.start_btn,0,1,1,2)
        self.bottom_layout.addWidget(QWidget(),0,3)
        self.main_layout.addLayout(self.top_layout,0,0)
        self.main_layout.addLayout(self.middle_layout,1,0,2,1)
        self.main_layout.addLayout(self.bottom_layout,3,0)
        self.setLayout(self.main_layout)

    def initSlot(self):
        self.start_btn.clicked.connect(self.start_clicked)

    # スタートボタンが押されたときの処理
    @Slot()
    def start_clicked(self):
        res = QMessageBox.question(self, '開始します', '出席を開始しますか?')
        if res == QMessageBox.Yes:
            self.clicked_signal.emit(self.kamoku_combo.currentText(),self.kaisu_combo.currentText())

