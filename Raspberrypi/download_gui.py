import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class DownloadGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dwnwidget = DownloadWidget()
        self.setCentralWidget(self.dwnwidget)


class DownloadWidget(QWidget):
    def __init__(self,parent=None):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 
        self.label = QLabel("出席管理システム\n履修者リストダウンロード")
        self.label.setFont(QFont('メイリオ',40))
        self.label.setAlignment(Qt.AlignCenter)
        # ダウンロードボタン
        self.dwnbtn = QPushButton(self)
        self.dwnbtn.setText('ダウンロード')
        self.dwnbtn.clicked.connect(self.download_risyusya_list)
        # 科目コンボボックス
        # 科目一覧
        self.kamoku = ['F1','F2','F3','F4','F5','M1','M2','M3','M4','M5']
        self.kamoku_combo = QComboBox()
        self.kamoku_combo.setFixedSize(200,200)
        for s in self.kamoku:
            self.kamoku_combo.addItem(s)

        # ウィジェット配置
        self.top_layout = QVBoxLayout()
        self.select_layout = QVBoxLayout()
        self.select_layout.addWidget(self.kamoku_combo)
        self.top_layout.addWidget(self.label)
        self.top_layout.addLayout(self.select_layout)
        self.top_layout.addWidget(self.dwnbtn)
        self.setLayout(self.top_layout)

    @Slot()
    def download_risyusya_list(self):
        flag = True
        print('ここにダウンロード処理を書く')

        # ダウンロード成功時の処理
        if flag:
            res = QMessageBox.information(self, 'ダウンロード完了', '履修者リストのダウンロードが成功しました',QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DownloadGUI()
    ex.show()
    sys.exit(app.exec_())
