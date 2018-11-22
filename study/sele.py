# -*- coding: utf-8 -*-
# author: WangYun 


from selenium import webdriver


def main():
    browser = webdriver.Firefox()
    browser.get("http://www.baidu.com")

    driver = webdriver.Chrome()
    driver.get("http://www.baidu.com")
    pass


if __name__ == '__main__':
    main()