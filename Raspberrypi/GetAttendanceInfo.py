#最終変更日7月14日
#時間によって出席・遅刻・欠席を判別するプログラム
#CurrentTimeに「'IDを読み込んだ時間' ex)'08:46:05'」, SubjectRuleに「科目ルールの格納されたリスト」, SGに「出席限度時刻」, TGに「遅刻限度時刻」を渡す
#CurrentTimeに渡した時間によって出席・遅刻・欠席を判別し結果を文字列で返す

import SplitCharacter
import time_compare
import ReadCsv
import os

def GAInfo(CurrentTime, SubjectRule, SG, TG):
    #渡された文字列を「:」で区切る
    #ex)'08:46:05' ⇒ '08', '46', '05'
    #PP[0]は時, PP[1]は分, PP[2]は秒の情報を持つ
    PP = SplitCharacter.split(CurrentTime)

    T = time_compare.TimeCompare(SubjectRule[0][1], SG, TG, 0)

    #渡された時間に応じて出席・遅刻・欠席を判別
    #print(T.is_syusseki(time_compare.datetime.time(int(PP[0]), int(PP[1]), int(PP[2]))))
    if T.is_syusseki(time_compare.datetime.time(int(PP[0]), int(PP[1]), int(PP[2]))) == True:
        return '出席'
    #print(T.is_tikoku(time_compare.datetime.time(int(PP[0]), int(PP[1]), int(PP[2]))))
    elif T.is_tikoku(time_compare.datetime.time(int(PP[0]), int(PP[1]), int(PP[2]))) == True:
        return '遅刻'
    #print(T.is_kesseki(time_compare.datetime.time(int(PP[0]), int(PP[1]), int(PP[2]))))
    #elif T.is_kesseki(time_compare.datetime.time(int(PP[0]), int(PP[1]), int(PP[2]))) == True:
    else:
        return '欠席'

if __name__ == '__main__':
    RulePath = os.path.abspath('kisoku_F2.csv')
    SubjectRule = []
    ReadCsv.readCsv(RulePath, SubjectRule)

    SG = int(SubjectRule[0][2])
    TG = int(SubjectRule[0][3])

    #出席
    Time = '08:46:05'
    AInfo = GAInfo(Time, SubjectRule, SG, TG)
    print(AInfo)
    
    #遅刻
    Time = '09:22:56'
    AInfo = GAInfo(Time, SubjectRule, SG, TG)
    print(AInfo)

    #欠席
    Time = '09:51:32'
    AInfo = GAInfo(Time, SubjectRule, SG, TG)
    print(AInfo)
