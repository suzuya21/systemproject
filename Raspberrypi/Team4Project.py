import ReadCsv
import IdCompare
import CreateCsv
import WriteCsv
import GenerateInformation
import time_compare
import SplitCharacter
import os

SubjectID = 'F1'

#ListPathに履修者データのパスを代入
ListPath = os.path.abspath(f'risyu_{SubjectID}.csv')
#print(ListPath)

#RulePathに科目ルールのパスを代入
RulePath = os.path.abspath(f'kisoku_{SubjectID}.csv')
#print(RulePath)

#risyu_{SubjectID}.csvの読み込み
Registerlist = []
ReadCsv.readCsv(ListPath, Registerlist)
#print(Registerlist)

#kisoku_{SubjectID}.csvの読み込み
SubjectRule = []
ReadCsv.readCsv(RulePath, SubjectRule)
#print(SubjectRule)

#Countに講義回数を代入
Count = SubjectRule[0][0]

#動作確認用
#Count = 11

#SGに出席限度時間を代入
SG = int(SubjectRule[0][2])
#TGに遅刻限度時間を代入
TG = int(SubjectRule[0][3])

#新しいcsvファイルを作成する
CreateCsv.create(SubjectID, Count)

#GetInfoリストにGenerateInformationで作成したデータを格納する
GetInfo = []
#pathに{SubjectID}-AttendanceList{Count}.csvのパスを代入
path = os.path.abspath(f'{SubjectID}/{SubjectID}-AttendanceList{Count}.csv')
ReadCsv.readCsv(path, GetInfo)
#print(GetID)

for i in range(len(GetInfo)):
    ID = GetInfo[i][2]
    #print(ID)

    a = IdCompare.idCompare(Registerlist, ID)
    #print(a)

    #履修者リストに無いIDが読み込まれたときの処理
    if a == []:
        print('あなたは履修者ではありません.')
        #以降の処理を無視し最初に戻る
        continue

    #time = GetInfo[i][1]
    #print(time)
    PP = SplitCharacter.split(GetInfo[i][1])
    #print(PP)

    T = time_compare.TimeCompare(SubjectRule[0][1], SG, TG, 0)
    #print(T.is_syusseki(time_compare.datetime.time(int(PP[0]), int(PP[1]), int(PP[2]))))
    if T.is_syusseki(time_compare.datetime.time(int(PP[0]), int(PP[1]), int(PP[2]))) == True:
        #要素に出席を追加
        a.append('出席')
    #print(T.is_tikoku(time_compare.datetime.time(int(PP[0]), int(PP[1]), int(PP[2]))))
    if T.is_tikoku(time_compare.datetime.time(int(PP[0]), int(PP[1]), int(PP[2]))) == True:
        a.append('遅刻')
    #print(T.is_kesseki(time_compare.datetime.time(int(PP[0]), int(PP[1]), int(PP[2]))))
    if T.is_kesseki(time_compare.datetime.time(int(PP[0]), int(PP[1]), int(PP[2]))) == True:
        a.append('欠席')

    #{SubjectID}_{Count}.csvに書き込み
    WriteCsv.write(a, SubjectID, Count)