#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json

def main_test():
    filepath = os.getcwd()
    filepath = os.path.join(filepath, 'CTA_setting.json')

    with open(filepath, 'rb') as f:
        setting = f.read()
        if type(setting) is not str:
            setting = str(setting, encoding='utf8')
        setting = json.loads(setting)



if __name__ == '__main__':
    main_test()