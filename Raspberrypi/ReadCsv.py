#最終変更日7月12日
#csvファイルを読み込むプログラム
#fに「'読み込みたいファイルのファイル名'」, listに「リスト(list型)」を渡す
#渡した「リスト」にcsvファイルの中身が格納される
import csv

#csvファイルを読み込む関数
def readCsv(f, list):
    with open(f, "r", encoding = "utf_8") as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            list.append(row)