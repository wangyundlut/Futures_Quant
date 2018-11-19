# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/8/21 20:57
import datetime

class trade_timemode:
    def __init__(self):
        pass
    def mode_date_time_series(self, date, mode):
        """
        1 模式： 正常日盘
        2 模式： 夜盘11点
        3 模式：夜盘11点半
        4 模式：夜盘1点
        5 模式：夜盘2点半
        """
        mode1 =[
               ['09:00:00', '10:15:00'],
               ['10:30:00', '11:30:00'],
               ['13:30:00', '15:00:00'],
               ]
        mode2 =[
               ['21:00:00', '23:00:00'],
               ['09:00:00', '10:15:00'],
               ['10:30:00', '11:30:00'],
               ['13:30:00', '15:00:00'],
               ]
        mode3 =[
               ['21:00:00', '23:30:00'],
               ['09:00:00', '10:15:00'],
               ['10:30:00', '11:30:00'],
               ['13:30:00', '15:00:00'],
               ]
        mode4 =[
               ['21:00:00', '23:59:59'],
               ['00:00:00', '01:00:00'],
               ['09:00:00', '10:15:00'],
               ['10:30:00', '11:30:00'],
               ['13:30:00', '15:00:00'],
               ]
        mode5 =[
               ['21:00:00', '23:59:59'],
               ['00:00:00', '02:30:00'],
               ['09:00:00', '10:15:00'],
               ['10:30:00', '11:30:00'],
               ['13:30:00', '15:00:00'],
               ]
        time_series = []
        yest = datetime.datetime.strptime(date, '%Y-%m-%d') \
               - datetime.timedelta(1, 0)
        yest = datetime.datetime.strftime(yest, '%Y-%m-%d')
        if mode == '1':
            for t in mode1:
                t_s = t[0]
                t_e = t[1]
                time_series.append([date + ' ' + t_s, date + ' ' + t_e])
        elif mode == '2':
            for t in mode2:
                t_s = t[0]
                t_e = t[1]
                if t_s >= '21:00:00' and t_e <= '23:59:59':
                    t_s = yest + ' ' + t_s
                    t_e = yest + ' ' + t_e
                else:
                    t_s = date + ' ' + t_s
                    t_e = date + ' ' + t_e
                time_series.append([t_s, t_e])
        elif mode == '3':
            for t in mode3:
                t_s = t[0]
                t_e = t[1]
                if t_s >= '21:00:00' and t_e <= '23:59:59':
                    t_s = yest + ' ' + t_s
                    t_e = yest + ' ' + t_e
                else:
                    t_s = date + ' ' + t_s
                    t_e = date + ' ' + t_e
                time_series.append([t_s, t_e])
        elif mode == '4':
            for t in mode4:
                t_s = t[0]
                t_e = t[1]
                if t_s >= '21:00:00' and t_e <= '23:59:59':
                    t_s = yest + ' ' + t_s
                    t_e = yest + ' ' + t_e
                else:
                    t_s = date + ' ' + t_s
                    t_e = date + ' ' + t_e
                time_series.append([t_s, t_e])
                time_series[0][1] = time_series[1][1]
                time_series.remove(time_series[1])
        elif mode == '5':
            for t in mode5:
                t_s = t[0]
                t_e = t[1]
                if t_s >= '21:00:00' and t_e <= '23:59:59':
                    t_s = yest + ' ' + t_s
                    t_e = yest + ' ' + t_e
                else:
                    t_s = date + ' ' + t_s
                    t_e = date + ' ' + t_e
                time_series.append([t_s, t_e])
                time_series[0][1] = time_series[1][1]
                time_series.remove(time_series[1])
        return time_series

    def minute_1_series(self, date, mode):
        time_series = self.mode_date_time_series(date, mode)

    def minute_5_series(self, date, mode):
        pass
    def minute_30_series(self, date, mode):
        pass
    def minute_60_series(self, date, mode):
        pass
    def day_series(self, date, mode):
        pass



if __name__ =='__main__':
    self = trade_timemode()
    self.mode_date_time_series('2018-02-02', '2')