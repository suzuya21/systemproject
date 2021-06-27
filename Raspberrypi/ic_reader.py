import sys
import threading
import ctypes
"""
使用方法
val = ICReader()
val.on_connect(func)
val.start()
"""
# カードリーダ部分
class ICReader(threading.Thread):
    def __init__(self,widget):
        #super(ICReader,self).__init__()
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.setDaemon(True)
        self.last_idm = 12 # 直近のIDm
        self.checked_idm_list = list() # チェック済みIDmリスト
        self.func = lambda :0
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
        from termios import tcflush, TCIFLUSH
        tcflush(sys.stdin, TCIFLUSH)
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
            print("入力開始")
            self.idm = self.read_id()
            self.func(self.idm)
            print("入力終了")
            self.event.wait()
            self.event.clear()
            continue
            # IDmの重複チェック
            if not self.is_duplicated_idm(self.idm):
                self.checked_idm_list.append(self.idm)
                self.wm.readidm.emit(self.idm)
            else:
                self.wm.readidm.emit(self.idm+"はすでにかざしてらっしゃる")
                #self.wm.update_text(self.idm+"はすでにかざしてらっしゃる")

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
   
    # 例外を起こすことで強制的にスレッドを止める
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,\
              ctypes.py_object(SystemExit))
        print('スレッド停止')
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
