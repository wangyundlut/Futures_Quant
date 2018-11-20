#!/usr/bin/python
# -*- coding: UTF-8 -*-


# encoding: UTF-8
# 系统模块

from queue import Queue, Empty
from threading import *

class dog:
    def __init__(self):
        print('hello i')
    def buck(self):
        print('buck')

class mydog(dog):
    def __init__(self):
        dog.__init__(self)
        print('what')
    def buck(self):
        print('is this right')



if __name__ == '__main__':
    d = mydog()
    d.buck()
