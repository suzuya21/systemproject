import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import ctypes
import requests
import time
import threading
from ic_reader import ICReader 
from attendance_management import AttendanceManagement,AttendIdent

# ラズパイ公式7インチタッチパネル 800 x 480 60fps

# メインウィンドウ
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.start_widget = StartWidget()
        #self.common = TestWidget()
        self.setCentralWidget(self.start_widget)
        #self.setCentralWidget(self.common)
        self.start_widget.changeWidget.connect(lambda x,y:self.change(x,y))

    # 出席状況表示用ウィジェットに切り替え
    @Slot(str,int)
    def change(self,kamoku,kaisu):
        try:
            self.gamelikeWidget = GamelikeWidget(kamoku,kaisu)
            self.gamelikeWidget.returnsignal.connect(self.return_toppage)
            #self.reader = ICReader(self.gamelikeWidget)
            #self.reader.start_read()
            #self.reader.start()
            self.setCentralWidget(self.gamelikeWidget)
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


# 共通ウィジェット (使うかもしれないし，多分使わない)
class CommonWidget(QWidget):
    def __init__(self):
        super().__init__()
        #self.initUI()

    def initUI(self):
        # 終了ボタン
        self.exitBtn = QPushButton('x')
        self.exitBtn.setFixedSize(200,100)
        self.exitBtn.clicked.connect(self.exitWindow)

        # 共通範囲
        self.commonLayout = QVBoxLayout()

        # ヘッダ？レイアウト
        self.headerLayout = QHBoxLayout()
        self.headerLayout.setAlignment(Qt.AlignRight)
        self.headerLayout.addWidget(self.exitBtn)

        # コンテンツ部分の
        self.layout = QHBoxLayout()

        # メインコンテンツwidget
        self.content = QWidget()
        self.content.setLayout(self.layout)
        self.content.setFixedSize(500,500)

        # レイアウトに追加
        #self.commonLayout.addWidget(self.exitBtn)
        self.commonLayout.addLayout(self.headerLayout)
        self.commonLayout.addWidget(self.content)

        self.setLayout(self.commonLayout)

    @Slot()
    def exitWindow(self):
        res = QMessageBox.question(self, '終了します', '出席管理を終わりまする．')
        if res == QMessageBox.Yes:
            self.close()
            QCoreApplication.quit()


# 起動時の画面
class StartWidget(QWidget):
    changeWidget = Signal(str,int)
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 
        self.label = QLabel("出席管理システム")
        self.label.setFont(QFont('メイリオ',40))
        self.label.setAlignment(Qt.AlignCenter)
        # スタートボタン
        self.btn = QPushButton("授業開始")
        self.btn.clicked.connect(self.emit_clicked)
        self.btn.setFixedSize(200,200)
        # 科目コンボボックス
        self.kamoku = ['F1','F2','F3','F4','F5','M1','M2','M3','M4','M5']
        self.kamoku_combo = QComboBox()
        self.kamoku_combo.setFixedSize(200,200)
        for s in self.kamoku:
            self.kamoku_combo.addItem(s)
        # 回数コンボボックス
        self.kaisu = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        self.kaisu_combo = QComboBox()
        self.kaisu_combo.setFixedSize(200,200)
        for s in self.kaisu:
            self.kaisu_combo.addItem(str(s))

        # layout
        self.main_layout = QVBoxLayout()
        self.combo_layout = QHBoxLayout()
        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(self.combo_layout)
        self.btn_layout = QHBoxLayout()
        self.btn_layout.addStretch()
        self.btn_layout.addWidget(self.btn)
        self.btn_layout.addStretch()
        self.main_layout.addLayout(self.btn_layout)
        self.combo_layout.addWidget(self.kamoku_combo)
        self.combo_layout.addWidget(self.kaisu_combo)
        self.setLayout(self.main_layout)

    @Slot()
    def emit_clicked(self):
        print(self.kaisu_combo.currentText())
        self.changeWidget.emit(str(self.kamoku_combo.currentText()),int(self.kaisu_combo.currentText()))


class GamelikeWidget(QWidget):
    readidm:Signal = Signal(str) # idmを読み取ったときのsignal
    returnsignal:Signal = Signal() # 画面をトップページに戻したいときのsignal
    def __init__(self,kamoku,kaisu,parent=None):
        super(GamelikeWidget,self).__init__(parent)
        # ラズパイ公式7インチタッチパネル 800 x 480 60fps
        self._height = 600
        self._width = 1000
        self.reader = ICReader(self)
        self.reader.on_connect(self.readidm.emit) # 読み取り部分に関数登録
        self.reader.start() # 読み取り開始
        self.attendance_management = AttendanceManagement(kamoku,kaisu)
        self.attendance_management.get_risyu_list('test.csv')
        self.risyusya_number = self.attendance_management.risyu_number # 履修者の数
        self.enemyHP = self.attendance_management.risyu_number # HP上限は履修者の数
        self.myHP = self.attendance_management.risyu_number # HP上限は履修者の数
        self.initUI()

    def initUI(self):
        self.setFixedSize(self._width,self._height)
        # バックグラウンド(ポケモン風画像)
        self.background = QLabel(self)
        self.background.setFixedSize(self._width,self._height)
        self.background.setPixmap(QPixmap('./UI.png'))
        # 敵HP
        self.enemyHPbar = QProgressBar(self)
        self.enemyHPbar.setFixedSize(240,20)
        self.enemyHPbar.setMaximum(self.risyusya_number)
        self.enemyHPbar.setValue(self.enemyHP)
        self.enemyHPbar.setFormat('%v/'+str(self.risyusya_number))
        self.enemyHPinfo = QLabel(self)
        self.enemyHPinfo.setText(str(self.enemyHP)+'  /  '+str(self.risyusya_number))
        self.enemyHPinfo.setFont(QFont("メイリオ",25))
        self.enemyHPinfo.setFixedSize(140,30)
        # 自分HP
        self.myHPbar = QProgressBar(self)
        self.myHPbar.setFixedSize(240,20)
        self.myHPbar.setMaximum(self.risyusya_number)
        self.myHPbar.setValue(self.myHP)
        self.myHPbar.setFormat('%v/'+str(self.risyusya_number))
        self.myHPinfo = QLabel(self)
        self.myHPinfo.setFont(QFont("メイリオ",25))
        self.myHPinfo.setText(str(self.myHP)+'  /  '+str(self.risyusya_number))
        # テキスト欄
        self.text = QLabel(self)
        self.text.setFixedSize(900,200)
        self.text.setStyleSheet('background-color: red;')
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
        self.enemyHPbar.move(150,110)
        self.enemyHPinfo.move(180,130)
        self.myHPbar.move(620,330)
        self.myHPinfo.move(640,340)
        self.text.move(50,450)
        self.exitBtn.move(800,450)
        self.returnBtn.move(800,500)
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
        time.sleep(2)
        self.init_text()
        print("並列処理再開 on GamelikeWidget.update_text")
        self.reader.event.set()

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
    ex = MainWindow()
    #ex = GamelikeWidget()
    ex.show()
    #reader = ICReader(ex)
    #reader.start_read()
    sys.exit(app.exec_())

