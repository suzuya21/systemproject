import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import ctypes
import requests
import time
import threading
import datetime
from ic_reader import ICReader 
from attendance_management import AttendanceManagement,AttendIdent
from shadow_effect import ShadowEffect
from totalization_widget import TotalizationWidget
from clock_widget import ClockWidget
from syuketu_widget import SyussekiWidget
from start_widget import StartWidget

# ラズパイ公式7インチタッチパネル 800 x 480 60fps

# メインウィンドウ
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('出席管理')
        self.initUI()

    def initUI(self):
        # self.setStyleSheet('background-color:white;')
        self.setObjectName('MainWindow')
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.start_widget = StartWidget()
        #self.common = TestWidget()
        self.setCentralWidget(self.start_widget)
        self.start_widget.clicked_signal.connect(self.change)
        #self.setCentralWidget(self.common)
        # self.start_widget.changeWidget.connect(lambda x,y:self.change(x,y))
        self.status.hide
        self.resize(800,500)
        # self.start_widget.setFixedSize(800,500)
        # self.start_widget.setGraphicsEffect(ShadowEffect(self))

    def resizeEvent(self, event):
        super(MainWindow, self).resizeEvent(event)
        # self.start_widget.setFixedSize(self.width(),self.height())
        print(self.height(),self.width())

    # 出席状況表示用ウィジェットに切り替え
    @Slot(str,int)
    def change(self,kamoku,kaisu):
        try:
            self.main = MainWidget()
            self.setCentralWidget(self.main)
        except:
            import traceback
            traceback.print_exc()

    # トップページに戻る
    @Slot()
    def return_toppage(self):
        self.gamelikeWidget = '' # この時点でGamelikeWidget()は消される，しかし並列処理しているのIC読み取り部分は止まらない
        self.start_widget = StartWidget()
        self.start_widget.changeWidget.connect(lambda x,y:self.change(x,y))
        self.setCentralWidget(self.start_widget)


# 起動時の画面
class MainWidget(QWidget):
    changeWidget = Signal(str,int)
    def __init__(self):
        super().__init__()
        # self.setFixedSize(800,480)
        self.ic_reader = ""#icリーダーオブジェクト
        self.uketuke = True
        self.initUI()
        self.initSlot()
        self.setStyle(QStyleFactory.create('WindowsXP'))

    def initUI(self):
        # 上段
        # タイトルラベル
        self.label = QLabel("<html>出席管理 <img src='images/fileio2.png'></html>")
        self.label.setFont(QFont('メイリオ',30))
        self.label.setAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        self.label.setObjectName('TitleLabel')
        # self.label.setStyleSheet("border-radius:40%;color:black;background-color: white;")
        self.label.setGraphicsEffect(ShadowEffect(self))
        self.label.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        # 時計
        self.clock = ClockWidget(20)
        self.clock.start()

        # 中層
        # なまえラベル
        self.name_label = QLabel('待機中')
        self.name_label.setFont(QFont('メイリオ',30))
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setStyleSheet("border-radius:40%;color:black;background-color: white;")
        self.name_label.setGraphicsEffect(ShadowEffect(self))
        self.name_label.setMargin(20)
        self.name_label.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        # 出席ラベル
        self.syusseki_label = SyussekiWidget()
        self.syusseki_label.setText('')

        # 戻るボタン
        self.return_btn = QPushButton("戻る")
        self.return_btn.setIcon(QPixmap("images/return.png"))
        self.return_btn.setIconSize(QSize(60,60))
        self.return_btn.setGraphicsEffect(ShadowEffect(self))
        self.return_btn.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.return_btn.setObjectName('ReturnBtn')
        # self.return_btn.setStyleSheet("border-radius:30%;color:black;background-color: white;")
        self.return_btn.setFont(QFont("メイリオ",20))
        # 終了ボタン
        self.exit_btn = QPushButton("終了")
        self.exit_btn.setGraphicsEffect(ShadowEffect(self))
        self.exit_btn.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.exit_btn.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.exit_btn.setObjectName('ExitBtn')
        # self.exit_btn.setStyleSheet("border-radius:30%;color:white;background-color: black;")
        self.exit_btn.setFont(QFont("メイリオ",20))
        self.exit_btn.clicked.connect(lambda :(self.name_label.setText("スズキイチロウタロ\nウジロウ"),self.syusseki_label.setText("欠席")))
        # スタートボタン
        self.btn = QPushButton("授業開始")
        self.btn.clicked.connect(self.emit_clicked)
        self.btn.setFixedSize(200,80)
        btn_css = 'QPushButton{border-radius:20%;color:black;background-color: white;}QPushButton:hover{background-color: red;}'
        self.btn.setStyleSheet(btn_css)
        self.btn.setGraphicsEffect(ShadowEffect(self))
        # 科目コンボボックス
        self.kamoku = ['F1','F2','F3','F4','F5','M1','M2','M3','M4','M5','s2','s3','s4','s5','m1','m2','l3','m4','m5']
        self.kamoku_combo = QComboBox()
        self.kamoku_combo.setFont(QFont('メイリオ',20))
        self.kamoku_combo.setFixedSize(200,130)
        for s in self.kamoku:
            self.kamoku_combo.addItem(s)
        self.kamoku_combo.setStyleSheet("overflow:hidden;appearance:none;border-radius:30%; padding: 3px 15px 3px 15px;color:black;background-color: white;")
        self.kamoku_combo.setGraphicsEffect(ShadowEffect(self))
        # 回数コンボボックス
        self.kaisu = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        self.kaisu_combo = QComboBox()
        self.kaisu_combo.setFixedSize(200,130)
        for s in self.kaisu:
            self.kaisu_combo.addItem(str(s))
        # 集計
        self.syukei = TotalizationWidget()
        self.syukei.setGraphicsEffect(ShadowEffect(self))
        # layout
        self.main_layout = QVBoxLayout()
        self.combo_layout = QHBoxLayout()
        self.clockLayout = QVBoxLayout()
        self.clockLayout.addWidget(self.clock)
        self.clockLayout.addWidget(QWidget())
        # self.clockLayout.addStretch(1)
        self.headerLayout = QGridLayout()
        self.headerLayout.setContentsMargins(0,0,20,0)
        # self.headerLayout.setColumnStretch(0,1)
        self.headerLayout.addWidget(QWidget(),0,0) # stretchの使い方がわからないので無理やり
        self.headerLayout.addWidget(self.label,0,1,1,3)
        # self.headerLayout.setColumnStretch(4,1)
        self.headerLayout.addLayout(self.clockLayout,0,5)
        self.main_layout.setSpacing((self.height()+self.width())/20)
        self.main_layout.setMargin((self.height()+self.width())/20)
        self.main_layout.setSpacing(40)
        self.main_layout.setMargin(40)
        # self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(self.headerLayout)
        # self.main_layout.addStretch(1)
        # self.main_layout.addLayout(self.combo_layout)
        # self.main_layout.addStretch(1)
        self.btn_layout = QHBoxLayout()
        self.btn_layout.addStretch()
        self.btn_layout.addWidget(self.btn)
        self.btn_layout.addStretch()
        # self.main_layout.addLayout(self.btn_layout)

        # middle
        self.middleLayout = QGridLayout()
        self.middleLayout.setContentsMargins(25,0,25,0)
        # self.middleLayout.setMargin(100)
        # self.middleLayout.setSpacing(100)
        self.middleLayout.addWidget(self.name_label,0,0,1,2)
        self.middleLayout.addWidget(self.syusseki_label,0,2,1,1)

        # self.main_layout.addStretch(1)
        # 最下段
        self.footerLayout = QGridLayout()
        self.footerLayout.setContentsMargins(10,0,10,0)
        self.footerLayout.addWidget(self.return_btn,1,0)
        # self.footerLayout.addWidget(QWidget(),1,1)
        self.footerLayout.addWidget(self.syukei,0,2,2,1)
        # self.footerLayout.addWidget(QWidget(),1,3)
        self.footerLayout.addWidget(self.exit_btn,1,4)

        self.main_layout.addLayout(self.middleLayout)
        # self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.footerLayout)
        self.combo_layout.addWidget(self.kamoku_combo)
        # self.combo_layout.addWidget(self.kaisu_combo)
        # self.combo_layout.addWidget(self.clock)

        self.setLayout(self.main_layout)
        # self.setGraphicsEffect(ShadowEffect(self))

    # スロット設定
    def initSlot(self):
        self.return_btn.clicked.connect(self.update_text)
        self.exit_btn.clicked.connect(self.exit_window)

    # 初期テキスト
    def init_text(self):
        self.name_label.setText('待機中')
        self.name_label.setFont(QFont('メイリオ',30))
        self.syusseki_label.setText('')
        self.uketuke = True
        print('init_text')

    # 画面を落とす
    @Slot()
    def exit_window(self):
        res = QMessageBox.question(self, '終了します', '出席管理を終わりまする．')
        if res == QMessageBox.Yes:
            self.close()
            QCoreApplication.quit()

    # 科目と回数を引数にシグナルを発火
    @Slot()
    def emit_clicked(self):
        print(self.kaisu_combo.currentText())
        self.changeWidget.emit(str(self.kamoku_combo.currentText()),int(self.kaisu_combo.currentText()))

    # ラベルとかその他とかをアップデート
    @Slot()
    def update_text(self):
        # syukketu = self.attendance_management.check_attendance(idm)
        # 2秒間だけ表示して元のテキストに戻す
        # 表示中にスキャンできないようにフラグを用意する
        if self.uketuke:
            self.uketuke = False
            self.name_label.setFont(QFont('メイリオ',14))
            self.name_label.setText('履修者として\n登録されていません')
            self.syusseki_label.setText('エラー')
            # self.name_label.setFont(QFont('メイリオ',30))
            # time.sleep(2)
            QTimer.singleShot(2000, self.init_text) # 二秒後に行う処理を書く
            # self.init_text()
            print("並列処理再開 on GamelikeWidget.update_text")
            # QTimer.singleShot(2000, self.reader.event.set)


class GamelikeWidget(QWidget):
    readidm:Signal = Signal(str) # idmを読み取ったときのsignal
    returnsignal:Signal = Signal() # 画面をトップページに戻したいときのsignal
    def __init__(self,kamoku,kaisu,parent=None):
        super(GamelikeWidget,self).__init__(parent)
        # ラズパイ公式7インチタッチパネル 800 x 480 60fps
        self._height = 480
        self._width = 800
        self.reader = ICReader(self)
        self.reader.on_connect(self.readidm.emit) # 読み取り部分に関数登録
        self.reader.start() # 読み取り開始
        self.attendance_management = AttendanceManagement(kamoku,kaisu)
        self.attendance_management.get_risyu_list('D:\work\systemproject\\test.csv')
        self.risyusya_number = self.attendance_management.risyu_number # 履修者の数
        self.enemyHP = self.attendance_management.risyu_number # HP上限は履修者の数
        self.myHP = self.attendance_management.risyu_number # HP上限は履修者の数
        self.initUI()

    def initUI(self):
        self.setFixedSize(self._width,self._height)
        # バックグラウンド(ポケモン風画像)
        self.background = QLabel(self)
        self.background.setFixedSize(self._width,self._height)
        self.background.setPixmap(QPixmap('C:\\Users\\user\\Downloads\\pokemonlike.png'))
        # 敵HP
        self.enemyHPbar = QProgressBar(self)
        self.enemyHPbar.setFixedSize(240,20)
        self.enemyHPbar.setMaximum(self.risyusya_number)
        self.enemyHPbar.setValue(self.enemyHP)
        self.enemyHPbar.setFormat('%v/'+str(self.risyusya_number))
        self.enemyHPinfo = QLabel(self)
        self.enemyHPinfo.setText(str(self.enemyHP)+'  /  '+str(self.risyusya_number))
        self.enemyHPinfo.setFont(QFont("メイリオ",25))
        self.enemyHPinfo.setFixedSize(300,35)
        # 自分HP
        self.myHPbar = QProgressBar(self)
        self.myHPbar.setFixedSize(240,20)
        self.myHPbar.setMaximum(self.risyusya_number)
        self.myHPbar.setValue(self.myHP)
        self.myHPbar.setFormat('%v/'+str(self.risyusya_number))
        self.myHPinfo = QLabel(self)
        self.myHPinfo.setFont(QFont("メイリオ",25))
        self.myHPinfo.setText(str(self.myHP)+'  /  '+str(self.risyusya_number))
        self.myHPinfo.setFixedSize(300,35)
        # テキスト欄
        self.text = QLabel(self)
        self.text.setFixedSize(900,200)
        # self.text.setStyleSheet('background-color: red;')
        self.text.setFont(QFont("メイリオ",40))
        self.init_text()

        #終了，戻るボタン
        self.exitBtn = QPushButton(self)
        self.exitBtn.setText("終了")
        self.exitBtn.setFixedSize(100,50)
        self.exitBtn.clicked.connect(self.exitWindow)
        self.exitBtn.setShortcut('q')
        self.returnBtn = QPushButton(self)
        self.returnBtn.setText("戻る")
        self.returnBtn.setFixedSize(100,50)
        self.returnBtn.clicked.connect(self.returnWindow)
        self.returnBtn.setShortcut('r')

        # 配置
        self.background.move(0,0)
        self.enemyHPbar.move(50,50)
        self.enemyHPinfo.move(50,80)
        self.myHPbar.move(500,240)
        self.myHPinfo.move(500,270)
        self.text.move(20,330)
        self.exitBtn.move(700,380)
        self.returnBtn.move(700,420)
        self.readidm.connect(lambda idm: self.update_text(idm))

    # 待機画面のラベルに遷移
    def init_text(self):
        self.text.setText("ICカードをかざすがよい")
        self.update()
        QCoreApplication.processEvents()

    # テキストの内容を割り当てる
    def assign_text(self,syukketu,idm):
        # 出席時には敵のHPが減る
        if syukketu == AttendIdent.Attendance:
            self.enemyHP = self.enemyHP-1
            if self.enemyHP < 0:
                self.enemyHP = 0
            self.enemyHPbar.setValue(self.enemyHP)
            self.enemyHPinfo.setText(str(self.enemyHP)+'  /  '+str(self.risyusya_number))
            #syukketu_table = ['出席','遅刻','欠席']
            self.text.setText(idm+'は出席することができました')
        # 欠席，遅刻時には自分のHPが減る
        elif syukketu == AttendIdent.Late or syukketu == AttendIdent.Absence:
            self.myHP = self.myHP-1
            if self.myHP < 0:
                self.myHP = 0
            self.myHPbar.setValue(self.myHP)
            self.myHPinfo.setText(str(self.myHP)+'  /  '+str(self.risyusya_number))
            #syukketu_table = ['出席','遅刻','欠席']
            if syukketu == AttendIdent.Late:
                self.text.setText(idm+'は遅刻することができました')
            else:
                self.text.setText(idm+'は欠席することができました')
        elif syukketu == AttendIdent.Already:
            self.text.setText(idm+'はすでにかざしてらっしゃる')
        else:
            self.text.setText(idm+'は履修者ではありません')
        self.update()
        QCoreApplication.processEvents()

    # ラベルとかその他とかをアップデート
    @Slot(str)
    def update_text(self,idm):
        syukketu = self.attendance_management.check_attendance(idm)
        self.assign_text(syukketu,idm)
        # 2秒間だけ表示して元のテキストに戻す
        # time.sleep(2)
        QTimer.singleShot(2000,self.init_text)
        # self.init_text()
        print("並列処理再開 on GamelikeWidget.update_text")
        QTimer.singleShot(2000,self.reader.event.set)

    @Slot()
    def exitWindow(self):
        res = QMessageBox.question(self, '終了します', '出席管理を終わりまする．')
        if res == QMessageBox.Yes:
            self.close()
            QCoreApplication.quit()

    @Slot()
    def returnWindow(self):
        res = QMessageBox.question(self, '終了します', '出席管理を終わりまする．')
        if res == QMessageBox.Yes:
            self.returnsignal.emit()
        self.reader.raise_exception()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    print(QStyleFactory.keys())
    ex = MainWindow()
    try:
        with open('main.css','r',encoding='utf-8') as f:
            css = f.read()
            app.setStyleSheet(css)
    except:
        print('css open error')
    #ex = GamelikeWidget()
    ex.show()
    #reader = ICReader(ex)
    #reader.start_read()
    sys.exit(app.exec_())

