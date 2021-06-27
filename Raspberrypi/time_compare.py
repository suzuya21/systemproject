import subprocess
import datetime

class TimeCompare():
    def __init__(self,start_time,syusseki,tikoku,kesseki):
        self._start_time = list(self.str_to_hour_minute(start_time)) # 09:00 24時間表記 文字列
        self._syusseki_time = 0 # 分
        self._tikoku_time = 0
        self._kesseki_time = 0
        self.syusseki_time=syusseki
        self.tikoku_time=tikoku
        self.kesseki_time=kesseki
        self._tmpdate = (2000,1,1)

    # 時間同期関数
    @staticmethod
    def sync_time(ntpserver):
        try:
            subprocess.call('ntpdate '+ntpserver) # sudoないと弾かれるから意味ないね
        except:
            return False
        return True

    @property
    def start_time(self):
        return self.int_to_datetime(self._start_time[0],self._start_time[1])
    @start_time.setter
    def start_time(self,hour,minute):
        self._start_time[0] = hour
        self._start_time[1] = minute
    @property
    def syusseki_time(self):
        return self._syusseki_time
    @syusseki_time.setter
    def syusseki_time(self,minute):
        tmp = self.add_time(self._start_time[0],self._start_time[1],0,minute)
        self._syusseki_time = self.int_to_datetime(tmp[0],tmp[1])
    @property
    def tikoku_time(self):
        return self._tikoku_time
    @tikoku_time.setter
    def tikoku_time(self,minute):
        tmp = self.add_time(self._start_time[0],self._start_time[1],0,minute)
        self._tikoku_time = self.int_to_datetime(tmp[0],tmp[1])
    @property
    def kesseki_time(self):
        return self._kesseki_time
    @kesseki_time.setter
    def kesseki_time(self,minute):
        tmp = self.add_time(self._start_time[0],self._start_time[1],0,minute)
        self._kesseki_time = self.int_to_datetime(tmp[0],tmp[1])

    # hour,minuteは範囲内の整数
    def int_to_datetime(self,hour,minute):
        now = datetime.datetime.now()
        tmpdate = now.year,now.month,now.day
        return datetime.datetime(tmpdate[0],tmpdate[1],tmpdate[2],hour,minute)

    # 時間の足し算
    def add_time(self,hour1,minute1,hour2,minute2):
        hour =int( hour1 + hour2 + int((minute1+minute2)/60) )% 24
        minute = int((minute1+minute2)%60)
        return hour,minute

    # '09:10' -> 9,10
    def str_to_hour_minute(self,time):
        return tuple([int(i) for i in time.split(':')])

    # 出席判定
    def is_syusseki(self):
        print('授業開始時間',self.start_time)
        print('出席終了時間',self.syusseki_time)
        print('遅刻終了時間',self.tikoku_time)
        print('欠席開始時間',self.kesseki_time)
        print('現在時刻',datetime.datetime.now())
        now = datetime.datetime.now()
        if now > self.start_time and now < self.syusseki_time:
            return True
        return False

    # 遅刻判定
    def is_tikoku(self):
        print(self.tikoku_time)
        now = datetime.datetime.now()
        if now > self.syusseki_time and now < self.tikoku_time:
            return True
        return False

    # 欠席判定(いらない)
    def is_kesseki(self):
        print(self.kesseki_time)
        now = datetime.datetime.now()
        if now > self.tikoku_time:
            return True
        return False
