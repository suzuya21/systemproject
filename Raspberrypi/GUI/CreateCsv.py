#最終変更日7月13日
#csvファイルを作成するプログラム
#SubjectIDに「'講義ID'」, Countに「'講義回数'」を渡す
#「講義ID_講義回数.csv」という名前のcsvファイルが作成される

import os
#csvファイルを作成する関数
def create(SubjectID, Count):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)),f'data/output/{SubjectID}_{Count}.csv')
    f = open(path, 'w', encoding = "utf_8", newline = '')
    f.close
