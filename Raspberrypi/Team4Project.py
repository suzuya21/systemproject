#最終変更日７月14日
#出席管理を行うプログラム
#SubjectIDに「'科目ID'」, Countに「'講義回数'」を渡す
#{SubjectID}_{Count}.csvが作成され, 出席情報が記録される

from Raspberrypi.GUI import GetStudentInfo, CreateCsv, ReadCsv, GetAttendanceInfo, WriteCsv
import os

def AttendanceManagement(SubjectID, Count):
    #履修者データと科目ルールが存在するか確認
    if not os.path.isfile(f'risyu_{SubjectID}.csv'):
        print(f'risyu_{SubjectID}.csv' + 'が存在しません.')
        return
    if not os.path.isfile(f'kisoku_{SubjectID}.csv'):
        print(f'kisoku_{SubjectID}.csv' + 'が存在しません.')
        return
    
    #ListPathに履修者データのパスを代入
    ListPath = os.path.abspath(f'risyu_{SubjectID}.csv')
    #print(ListPath)

    #RulePathに科目ルールのパスを代入
    RulePath = os.path.abspath(f'kisoku_{SubjectID}.csv')
    #print(RulePath)

    #risyu_{SubjectID}.csvの読み込み
    #渡された科目IDの履修者データを読み込む
    Registerlist = []
    ReadCsv.readCsv(ListPath, Registerlist)
    #print(Registerlist)

    #kisoku_{SubjectID}.csvの読み込み
    #渡された科目IDの科目ルールを読み込む
    SubjectRule = []
    ReadCsv.readCsv(RulePath, SubjectRule)
    #print(SubjectRule)

    #Countに講義回数を代入
    #Count = SubjectRule[0][0]

    #動作確認用
    #Count = 11

    #SGに出席限度時間を代入
    SG = int(SubjectRule[0][2])
    #TGに遅刻限度時間を代入
    TG = int(SubjectRule[0][3])

    #出席状況を記録するcsvファイルを作成する
    if not os.path.isfile(f'{SubjectID}_{Count}.csv'):
        CreateCsv.create(SubjectID, Count)

    #GenerateInformation.pyで作成されたデータが存在するか確認
    if not os.path.isfile(f'{SubjectID}/{SubjectID}-AttendanceList{Count}.csv'):
        print(f'{SubjectID}/{SubjectID}-AttendanceList{Count}.csv' + 'が存在しません.')
        return
    #GetInfoリストにGenerateInformationで作成したデータを格納する
    GetInfo = []
    #pathに{SubjectID}-AttendanceList{Count}.csvのパスを代入
    path = os.path.abspath(f'{SubjectID}/{SubjectID}-AttendanceList{Count}.csv')
    ReadCsv.readCsv(path, GetInfo)
    #print(GetID)

    i = 0
    while True:
        #os.system('PAUSE')
        input('続行するには何かキーを押してください')

        ID = GetInfo[i][2]
        # すでに登録されている場合Noneが返されるため数行後のappendで例外が起こる
        SInfo = GetStudentInfo.GSInfo(ID, Registerlist, SubjectID, Count)
        #すでに登録されていたIDもしくは履修者ではないIDが読み込まれたときの処理
        if SInfo == False:
            i += 1
            #os.system('PAUSE')
            input("SInfo is None")
            continue
        #print(SInfo)
        #print('名前：' + SInfo[1] + '　学籍番号：' + SInfo[2])

        Time = GetInfo[i][1]
        # elseがないので条件に引っかからない場合は戻り値がない，Noneなのでこの変数を使用する部分で例外が起こる
        AInfo = GetAttendanceInfo.GAInfo(Time, SubjectRule, SG, TG)
        print(AInfo)

        print(SInfo)
        SInfo.append(AInfo)
        
        #名前と学籍番号, 出席状況を表示できます
        print('名前：' + SInfo[1] + ' 学籍番号：' + SInfo[2] + ' ' + SInfo[3])

        #{SubjectID}_{Count}.csvに書き込み
        WriteCsv.write(SInfo, SubjectID, Count)

        i += 1

        # イベント発火
        # ここに発火させる
        # event.wait() 

        #終了処理
        #GUIの構成に合わせて変更してください
        if i > 99:
            break

    os.remove(f'{SubjectID}-読み取り履歴{Count}.csv')
    print('終了します.')

#処理が一通り終わった後は読み取り履歴の記録されたファイルを削除してください
#残ったままだと再度実行したときに, IDがすでに1度入力された状態になっているのでうまく動作しません
#もしくは93行のコメントアウトを外してください
if __name__ == '__main__':
    #科目ID, 講義回数を設定
    SID = 'F2'
    Count = '1'
    AttendanceManagement(SID, Count)
