#最終変更日6月21日
import csv
import SampleReadCardList

#取得したID
getID = '012E44A7A5185F5A'

#空のリスト
reference = []

#IDの比較
def refer():
    for i in SampleReadCardList.data:
        for j in i:
            if j == getID:
                reference = i
                break
    #ID所持者の情報表示
    #print(reference)
    return reference