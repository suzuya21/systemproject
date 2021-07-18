#最終変更日7月13日
#csvファイルを作成するプログラム
#SubjectIDに「'講義ID'」, Countに「'講義回数'」を渡す
#「講義ID_講義回数.csv」という名前のcsvファイルが作成される

#csvファイルを作成する関数
def create(SubjectID, Count):
    f = open(f'../data/output/{SubjectID}_{Count}.csv', 'w', encoding = "utf_8", newline = '')
    f.close
