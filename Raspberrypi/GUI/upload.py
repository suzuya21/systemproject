# PySide2のモジュールを読み込む
import sys
import os
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
#from tusin import post


# ウィンドウの見た目と各機能
class uploadWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__()

        self.label = QLabel(self) 
        self.label.setText("<html>アップロード <img src='upload_icon.png'></html>")  
        self.label.setFont(QFont('メイリオ',30))
        self.label.setStyleSheet("Qlabel")

        # コンボボックスオブジェクトの生成
        self.kougi_combobox = QComboBox(self)
        self.kougi_combobox.setFont(QFont('メイリオ',20))
        self.kougi_combobox.setFixedSize(200,130)
        #self.kougi_combobox.setStyleSheet("overflow:hidden; appearance:none; border-radius:30%; padding: 3px 15px 3px 15px;color:black;background-color: white;")

        self.count_combobox = QComboBox(self)
        self.count_combobox.setFont(QFont('メイリオ',20))
        self.count_combobox.setFixedSize(200,130)

        # 講義のコンボボックスの選択肢を追加
        self.kougi_combobox.addItems(['F1','F2','F3','F4','F5','M1','M2','M3','M4','M5'])
        # 講義回数のコンボボックスの選択肢を追加
        self.count_combobox.addItems(['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15'])

        #アップロードボタンを追加
        self.btn = QPushButton("ダウンロード")
        self.btn.clicked.connect(self.getfile)
        #self.btn.clicked.connect(self.upload_risyusya_list)
        self.btn.setFixedSize(200,80)
        btn_css = 'QPushButton{border-radius:20%;color:black;background-color: white;}QPushButton:hover{background-color: red;}'
        self.btn.setStyleSheet(btn_css)

        self.le = QLabel("Hello")

        #レイアウト
        self.Ver_layout = QVBoxLayout()
        self.Hol_layout = QHBoxLayout()
        self.Hol_layout.addWidget(self.kougi_combobox)
        self.Hol_layout.addWidget(self.count_combobox)
        self.Ver_layout.addWidget(self.label)
        self.Ver_layout.addLayout(self.Hol_layout)
        self.Ver_layout.addWidget(self.btn)
        self.setLayout(self.Ver_layout)
        self.setWindowTitle("出席管理-アップロード")



    #ファイル選択ダイアログを表示
    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"CSV files (*.csv)")
        self.le.setPixmap(QPixmap(fname))

    """
    def upload_risyusya_list(self):
        flag = True
        post()

        # ダウンロード成功時の処理
        if flag:
            res = QMessageBox.information(self, 'ダウンロード完了', '履修者リストのダウンロードが成功しました',QMessageBox.Ok)
    """

# アプリの実行と終了
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = uploadWindow()

    with open('upload.css','r') as f:
        style = f.read()
        app.setStyleSheet(style)

    ex.show()
    sys.exit(app.exec_())