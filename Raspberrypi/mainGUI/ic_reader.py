import sys
import threading
import ctypes
"""
使用方法
val = ICReader()
val.on_connect(func)
val.start()
"""
# カードリーダ読み取り部分
class ICReader(threading.Thread):
    def __init__(self,widget):
        #super(ICReader,self).__init__()
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.setDaemon(True) # 
        self.last_idm = '' # 直近のIDm
        self.checked_idm_list = list() # チェック済みIDmリスト
        self.func = lambda :0 # 読み取り時実行関数
        #self.wm = mainwindow.gameWidget
        self.wm = widget

    # 読み取り開始
    def run(self):
        self.readerloop()

    # 読み取りの並列処理を開始
    def start_read(self):
        th = threading.Thread(target=self.readerloop)
        th.setDaemon(True)
        th.start()

    # 読み取り
    def read_id(self):
        # この2行でinputを実行する前の入力をカットできる
        # from termios import tcflush, TCIFLUSH
        # tcflush(sys.stdin, TCIFLUSH)
        return input()

    # IDmの重複がないかのチェック False -> 重複なし, 
    def is_duplicated_idm(self,idm):
        for i in self.checked_idm_list:
            if idm == i:
                return True
        return False

    # 読み取りループ
    def readerloop(self):
        while True:
            print("DEBUG_入力開始")
            self.idm = self.read_id() # 読み取り開始
            self.func(self.idm) # 読み取ったidmを引数に実行
            print("DEBUG_入力終了")
            self.event.wait() # threadストップ
            self.event.clear()

    # 実行関数登録
    def on_connect(self,func):
        self.func = func

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            print(self._thread_id)
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                print(id)
                return id
   
    # 例外を起こすことで強制的にスレッドを止める 今のところ止まらない
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,\
              ctypes.py_object(SystemExit))
        print('スレッド停止')
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

