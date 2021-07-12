#最終変更日7月5日
import SampleReadCardList
import IdReference
import CreateCsv
import WriterCsv
import SendId
import os
import sys

import gM1
import ReadCsv
gM1

ListP = r'C:\Users\健太\.vscode\Raspberry Piの制御\講義データ(noWin)\履修者-M1.csv'
RuleP = r'C:\Users\健太\.vscode\Raspberry Piの制御\講義データ(noWin)\講義科目ルール.csv'

#csvファイルの読み込み
#学生リスト.csvが存在すれば読み込む
if(os.path.exists(r'C:\Users\健太\.vscode\Raspberry Piの制御\講義データ(noWin)\履修者-M1.csv')):
    SampleReadCardList.read(ListP)
else:
    sys.exit('ファイルが存在しません.')

#講義科目ルール.csvが存在すれば読み込む
if(os.path.exists(r'C:\Users\健太\.vscode\Raspberry Piの制御\講義データ(noWin)\講義科目ルール.csv')):
    SampleReadCardList.read(RuleP)
else:
    sys.exit('ファイルが存在しません.')

#print(SampleReadCardList.data)

#csvファイルを作成
CreateCsv.create()

exist = os.path.exists('F1_1.csv')
if exist == False:
    sys.exit('ファイルが存在しません.')

list = []
p = r'C:\Users\健太\.vscode\Raspberry Piの制御\M1\M1-20191007.csv'
ReadCsv.readCsv(p, list)
#print(list)

for i in range(len(list)):
    Id = list[i][2]
    #print(Id)

    a = IdReference.refer(Id)
    #print(a)

    #履修者リストに無いIDが読み込まれたときの処理
    if a == []:
        print('あなたは履修者ではありません.')
        #以降の処理を無視し最初に戻る
        continue

    time = list[i][1]
    #print(time)
    
    #要素に出席を追加
    a.append('出席')

    #M1_1.csvに書き込み
    WriterCsv.write(a)

'''
counter = 10
while(counter > 0):
    Id = SendId.sendID(counter)
    a = IdReference.refer(Id)

    #履修者リストに無いIDが読み込まれたときの処理
    if a == []:
        print('あなたは履修者ではありません.')
        counter -= 1
        #以降の処理を無視し最初に戻る
        continue

    #要素に出席を追加
    a.append('出席')

    
    a.append('遅刻')
    a.append('欠席')
    

    #F1_1.csvに書き込み
    WriterCsv.write(a)
    counter -= 1
'''