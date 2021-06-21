#最終変更日6月21日
import csv

#空のリスト
data = []

#csvファイルを読み込む関数
def read():
    with open(r"C:\Users\健太\.vscode\Raspberry Piの制御\講義データ(noWin)\学生リスト.csv", "r", encoding = "utf_8") as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            data.append(row)