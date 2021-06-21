#最終変更日6月21日
import csv
import IdReference

#csvファイルを作成する関数
def create(reference):
    f = open('出席者リスト.csv', 'w', encoding = "utf_8")
    writer = csv.writer(f)
    writer.writerow(reference)
    f.close