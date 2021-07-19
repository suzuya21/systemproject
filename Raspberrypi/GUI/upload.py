# PySide2のモジュールを読み込む
import sys
import os
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from tusin import post
from shadow_effect import ShadowEffect


class uploadMainWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()
        self.setObjectName('uploadMainWindow')
        self.main_widget = uploadWindow()
        self.setCentralWidget(self.main_widget)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.setFixedSize(800,480)
        statuslabel = QLabel()
        statuslabel.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        statuslabel.setOpenExternalLinks(True)
        statuslabel.setText('<a href="table.html">科目ID，科目名対応表</a>')
        self.status.addWidget(statuslabel)

class uploadWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__()

        #ウィンドウ
        self.setObjectName('uploadWindow')
        self.setFixedSize(800,480)

        #タイトル
        self.label = QLabel(self) 
        self.label.setText("アップロード")  
        #タイトルの装飾
        self.label.setFont(QFont('メイリオ',21))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName('title')
        self.label.setGraphicsEffect(ShadowEffect(self))

        # コンボボックスの生成+装飾
        self.kougi_combobox = QComboBox(self)
        self.kougi_combobox.setFont(QFont('メイリオ',20))
        self.kougi_combobox.setFixedSize(200,130)
        self.kougi_combobox.setObjectName('kougi_combobox')
        self.kougi_combobox.setGraphicsEffect(ShadowEffect(self))
        self.kougi_combobox.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)

        self.count_combobox = QComboBox(self)
        self.count_combobox.setFont(QFont('メイリオ',20))
        self.count_combobox.setFixedSize(200,130)
        self.count_combobox.setObjectName('count_combobox')
        self.count_combobox.setGraphicsEffect(ShadowEffect(self))
        self.count_combobox.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)

        # 講義のコンボボックスの選択肢を追加
        try:
            with open(os.path.abspath(f'../data/kamoku.csv'), 'r', encoding='utf-8') as f:
                import csv
                reader = csv.reader(f)
                next(reader)
                kamoku = [row [0] for row in reader]
        except:
            import traceback
            traceback.print_exc()
            kamoku = ['F1', 'F2', 'F3', 'F4_1', 'F4_2', 'M1', 'M2', 'M3', 'M4', 'T2', 'T3_1', 'T3_2', 'T4', 'T5', 'Th2', 'Th34',
         'Th5_1', 'Th5_2', 'W12', 'W3_1', 'W3_2', 'W4', 'W5_1', 'W5_2']
        self.kougi_combobox.addItems(kamoku)
        # 講義回数のコンボボックスの選択肢を追加
        self.count_combobox.addItems(['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15'])

        #アップロードボタンを追加
        self.btn = QPushButton("アップロード")
        #ファイル選択のダイアログが表示される
        #self.btn.clicked.connect(self.getfile)

        #コンボボックスから参照してファイルをアップロードする
        self.btn.clicked.connect(self.upload_risyusya_list)

        #アップロードボタンの装飾
        self.btn.setFixedSize(280,80)
        self.btn.setFont(QFont("メイリオ",20))
        self.btn.setObjectName('btn')
        self.btn.setGraphicsEffect(ShadowEffect(self))
        self.btn.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)

        #self.le = QLabel("Hello")

        #レイアウト
        self.main_layout = QVBoxLayout()
        self.main_layout = QGridLayout()
        self.top_layout = QGridLayout()
        self.middle_layout = QGridLayout()
        self.bottom_layout = QGridLayout()
        self.main_layout.setMargin(50)
        self.main_layout.setSpacing(50)
        self.top_layout.addWidget(QWidget(),0,0)
        self.top_layout.addWidget(self.label,0,1,1,3)
        self.top_layout.addWidget(QWidget(),0,4)
        self.middle_layout.addWidget(self.kougi_combobox,0,0,1,2)
        self.middle_layout.addWidget(QWidget(),0,2)
        self.middle_layout.addWidget(self.count_combobox,0,3,1,2)
        self.bottom_layout.addWidget(QWidget(),0,0)
        self.bottom_layout.addWidget(self.btn,0,1,1,2)
        self.bottom_layout.addWidget(QWidget(),0,3)
        self.main_layout.addLayout(self.top_layout,0,0)
        self.main_layout.addLayout(self.middle_layout,1,0,2,1)
        self.main_layout.addLayout(self.bottom_layout,3,0)
        self.setLayout(self.main_layout)
        self.setWindowTitle("出席管理-アップロード")



    """#ファイル選択ダイアログを表示
    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"CSV files (*.csv)")
        self.le.setPixmap(QPixmap(fname))
    """

    #コンボボックスから参照してファイルをアップロードする
    def upload_risyusya_list(self):
        flag = True
        flag = post(self.count_combobox.currentText(),self.kougi_combobox.currentText())

        # アップロード成功時の処理
        if flag:
            res = QMessageBox.information(self, 'アップロード完了', '出席データのアップロードが成功しました',QMessageBox.Ok)

        # アップロード失敗時の処理
        elif not flag:
            res = QMessageBox.information(self, 'アップロード失敗', '出席データのアップロードができませんでした',QMessageBox.Ok)

# アプリの実行と終了
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # ex = uploadWindow()
    ex = uploadMainWindow()

    #cssの読み込み
    with open('css/upload.css', 'r') as f:
        css = f.read()
        app.setStyleSheet(css)

    ex.show()
    sys.exit(app.exec_())
