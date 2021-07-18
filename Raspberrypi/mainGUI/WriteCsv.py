#最終変更日7月13日
#infoに「書き込みたいリスト(list型)」, SubjectIDに「'講義ID'」, Countに「'講義回数'」を渡す
#「講義ID_講義回数.csv」という名前のcsvファイルに「書き込みたいリスト」の要素が書き込まれる
import csv

#csvファイルに書き込む関数
def write(info, SubjectID, Count):
    with open(f'data/output/{SubjectID}_{Count}.csv', 'a', encoding = 'utf_8', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(info)
        f.close
