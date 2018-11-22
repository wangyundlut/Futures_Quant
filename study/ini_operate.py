# -*- coding: utf-8 -*-
# author: WangYun

import configparser
import os


def main():
    config = configparser.ConfigParser()
    file = os.getcwd()
    file = os.path.join(os.path.dirname(file), 'config', 'futures_info.ini')
    config.read(file)

    section_list = config.sections()
    print(section_list)

    option_list = config.options('J')
    print(option_list)

    item_list = config.items('J')
    print(item_list)

    db_host = config.get('J', 'trading_period')
    print(db_host)

    db_post = config.getint('J', 'port')
    config.getfloat('J', 'margin')
    print(db_post)


    config = configparser.ConfigParser()
    file = os.getcwd()
    file = os.path.join(file, 'study', 'config.ini')
    config.read(file)

    section_list = config.sections()
    print(section_list)

    option_list = config.options('baseconf')
    print(option_list)

    item_list = config.items('baseconf')
    print(item_list)

    db_host = config.get('baseconf', 'host')
    print(db_host)

    db_post = config.getint('baseconf', 'port')
    print(db_post)



if __name__ == '__main__':
    main()