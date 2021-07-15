#最終変更日7月14日
#読み込まれたIDが履修者のものであるか判別するプログラム
#IDに「'判別したいID'」, Registerlistに「履修者データの格納されたリスト」, SubjectIDに「'科目ID'」, Countに「'講義回数'」を渡す
#渡したIDが履修者のものであればその履修者の情報を返す
#渡したIDが履修者のものでなければ「あなたは履修者ではありません.」と表示し終了
#渡したIDがすでに読み込まれたものであれば「あなたはすでに登録済みです.」と表示し終了

import IdCompare
import ReadCsv
import os
import csv

def GSInfo(ID, Registerlist, SubjectID, Count):
    STInfo = IdCompare.idCompare(Registerlist, ID)
    #print(a)

    #履修者リストに無いIDが読み込まれたときの処理
    if STInfo == []:
        print('あなたは履修者ではありません.')
        #終了
        return False
    
    #{Team4Project.SubjectID}-読み取り履歴{Team4Project.Count}.csvがなければ作成
    if not os.path.isfile(f'{SubjectID}-読み取り履歴{Count}.csv'):
        print('ファイルを作成します.')
        f = open(f'{SubjectID}-読み取り履歴{Count}.csv', 'w', encoding = "utf_8", newline = '')
        f.close
    
    #空のリストHに{Team4Project.SubjectID}-読み取り履歴{Team4Project.Count}.csvの中身を格納
    H = []
    with open(f'{SubjectID}-読み取り履歴{Count}.csv', 'r', encoding = 'utf_8') as file:
        reader = csv.reader(file)
        for row in reader:
            H.append(row)
    
    #これまでに登録されたIDの表示
    #print(H)

    #IDがすでに登録されていたときの処理
    for i in H:
        for j in i:
            if ID == j:
                print('あなたはすでに登録済みです.')
                return False

    #print(H)

    #IDがまだ登録されていないときの処理
    #{Team4Project.SubjectID}-読み取り履歴{Team4Project.Count}.csvに登録されていないIDを書き込み
    with open(f'{SubjectID}-読み取り履歴{Count}.csv', 'a', encoding = 'utf_8', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow([ID])
        f.close
    
    #print(H)
    
    #履修者の情報を返す
    return STInfo
 
if __name__ == '__main__':
    ListPath = os.path.abspath('risyu_F1.csv')
    Registerlist = []
    ReadCsv.readCsv(ListPath, Registerlist)    
    print(GSInfo('012E44A7A5112853', Registerlist, 'F1', '11'))
    print(GSInfo('012E44A7A5188331', Registerlist, 'F1', '11'))
    print(GSInfo('012E44A7A518BB99', Registerlist, 'F1', '11'))
    #1回目と同じID
    print(GSInfo('012E44A7A5112853', Registerlist, 'F1', '11'))
    #履修者ではないID
    print(GSInfo('0000000000000000', Registerlist, 'F1', '11'))
