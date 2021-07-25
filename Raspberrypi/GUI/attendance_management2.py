"""
出席管理（内部処理）
生成した出席データを読み取り，出席情報を書き込む
Team4Project.pyの処理をThread継承クラスで書き直したもの
"""
import os
import sys
import threading
import ReadCsv
import CreateCsv
import WriteCsv
import GetStudentInfo
import GetAttendanceInfo

# kenta923 Team4Project.pyを並列処理するためにThread継承クラスとして実装
# set_kisoku,set_attendance_listを実行してからstart()
class AttendanceManagement(threading.Thread):
    def __init__(self,SubjectID,Count):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.setDaemon(True) # 

        # Team4Project.pyより
        self.SubjectID = SubjectID
        self.Count = Count
        self.datapath = os.path.join(os.path.dirname(os.path.dirname(__file__)),f'data')
        self.ListPath = os.path.abspath(os.path.join(self.datapath,f'input/risyu_{SubjectID}.csv'))
        self.RulePath = os.path.abspath(os.path.join(self.datapath,f'input/kisoku_{SubjectID}.csv'))
        self.path = os.path.abspath(os.path.join(self.datapath,f'{SubjectID}/{SubjectID}-AttendanceList{Count}.csv'))
        #self.path = os.path.abspath(f'../data/{SubjectID}/{SubjectID}-AttendanceList{Count}.csv')
        self.checked_list = [] # {}-読み取り履歴_{}.csvの代わり
        self.Registerlist = [] # 履修者リスト
        self.GetInfo = [] # GenerateInformationで作成したデータ

    # 読み取り履歴を削除，
    def __del__(self):
        # os.remove(f'{self.SubjectID}-読み取り履歴{self.Count}.csv')
        print('終了します.')

    # ファイルチェック等準備完了の場合True
    def is_ready(self):
        if not os.path.isfile(os.path.join(self.datapath,f'output/{self.SubjectID}_{self.Count}.csv')):
            CreateCsv.create(self.SubjectID, self.Count)
        return True

    # 必要なファイルがすべて存在する場合はTrue，それ以外False
    def is_existed_file(self):
        flag = True
        index = []
        if not os.path.isfile(self.ListPath):
            print(self.ListPath + 'が存在しません.')
            flag = False,
            index.append(0)
        if not os.path.isfile(self.RulePath):
            print(self.RulePath + 'が存在しません.')
            flag = False
            index.append(1)
        if not os.path.isfile(self.path):
            print(self.path + 'が存在しません.')
            flag = False
        return flag,index

    # 規則データセット
    def set_kisoku(self):
        self.Registerlist = []
        self.SubjectRule = []
        ReadCsv.readCsv(self.ListPath,self.Registerlist)
        ReadCsv.readCsv(self.RulePath,self.SubjectRule)
        # 出席限度，遅刻限度，授業開始時間
        self.SG = int(self.SubjectRule[0][2])
        self.TG = int(self.SubjectRule[0][3])
        self.ST = self.SubjectRule[0][1]

    # 出席リスト取得
    def set_attendance_list(self):
        self.GetInfo = []
        ReadCsv.readCsv(self.path, self.GetInfo)
        print(self.GetInfo)

    # 読み取り開始
    def run(self):
        self.readerloop()

    # 実行関数登録 func('name','出席')
    def on_connect(self,func):
        self.func = func

    def readerloop(self):
        i = 0
        while True:
            #os.system('PAUSE')
            # from termios import tcflush, TCIFLUSH
            # tcflush(sys.stdin, TCIFLUSH)
            input('続行するには何かキーを押してください')

            ID = self.GetInfo[i][2]
            # すでに登録されている場合Noneが返されるため数行後のappendで例外が起こる
            SInfo = GetStudentInfo.GSInfo(ID, self.Registerlist, self.SubjectID, self.Count)
            #すでに登録されていたIDもしくは履修者ではないIDが読み込まれたときの処理

            Time = self.GetInfo[i][1]
            # elseがないので条件に引っかからない場合は戻り値がない，Noneなのでこの変数を使用する部分で例外が起こる
            AInfo = GetAttendanceInfo.GAInfo(Time, self.SubjectRule, self.SG, self.TG)
            print(AInfo)


            if SInfo == 1:#履修者ではない
                SInfo = ('','','','not') # ダミーデータ
                #os.system('PAUSE')
                print("SInfo is None")
            #print(SInfo)
            elif len(SInfo) == 4:
                print(SInfo)
            #print('名前：' + SInfo[1] + '　学籍番号：' + SInfo[2])
            else:
                SInfo.append(AInfo)
                print(SInfo)
                #名前と学籍番号, 出席状況を表示できます
                print('名前：' + SInfo[1] + ' 学籍番号：' + SInfo[2] + ' ' + SInfo[3])

                #{SubjectID}_{Count}.csvに書き込み
                WriteCsv.write(SInfo, self.SubjectID, self.Count)

            i += 1

            # イベント発火
            # ここに発火させる
            # event.wait() 
            self.func(SInfo[1],SInfo[3])

            #終了処理
            #GUIの構成に合わせて変更してください
            if i > 99:
                break
            self.event.wait()
            self.event.clear()

if __name__=='__main__':
    SID = 'F2'
    Count = '1'
    a = AttendanceManagement(SID, Count)
    if not a.is_existed_file():
        exit(0)
    a.set_attendance_list()
    a.set_kisoku()
    if not a.is_ready():
        exit(0)
    a.readerloop()
