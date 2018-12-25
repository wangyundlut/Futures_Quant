#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime

def run1():
    while True:
        try:
            for i in range(10000):
                print('run1 :' + str(i))
            print('run1 end:' + datetime.datetime.now().strftime('%H:%M:%S.%f'))
            break
        except Exception:
            pass


def run2():
    while True:
        try:
            for i in range(10000):
                print('run2 :' + str(i))
            print('run2 end:' + datetime.datetime.now().strftime('%H:%M:%S.%f'))
            break
        except Exception:
            pass



def main_test():
    import threading
    t1 = threading.Thread(target=run1)
    t2 = threading.Thread(target=run2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == '__main__':
    main_test()

