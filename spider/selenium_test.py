# coding:utf-8
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

import os
import json
import traceback
import requests
import time

binary_location = '/usr/bin/google-chrome'
chrome_driver_binary = '/usr/bin/chromedriver'


def init_env(pid=0):
    options = webdriver.ChromeOptions()
    options.binary_location = binary_location  # 谷歌地址
    options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错

    options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
    options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    chromedriver = chrome_driver_binary
    os.environ["webdriver.chrome.driver"] = chromedriver
    brower = webdriver.Chrome(chrome_options=options, executable_path=chromedriver)
    return brower


def close_env(brower):
    brower.close()
    brower.quit()


def enter_main(driver):
    res = driver.get('http://service.bj.10086.cn/m/num/num/commonNum/showFontPage.action?busiCode=CKK')
    e = driver.find_element_by_id('ljgm')
    e.click()
    time.sleep(1.5)

def get_page_content(driver,key_str):
    input_box = driver.find_element_by_id('sousuoNumStr')
    input_box.send_keys(key_str)
    try:
        bt = driver.find_element_by_class_name('btn_sous')
        bt.click()
        time.sleep(2.5)

        text = driver.find_element_by_id('hm_lb').text
        return text

    except Exception as e:
        print(e)
        return ""

def loop_menu():
    brower = None
    try:
        brower = init_env()
        enter_main(brower)
        res = get_page_content(brower,"4420")
        print(res)

        if brower:
            close_env(brower)

    except Exception as e:
        traceback.print_exc()
        if brower:
            close_env(brower)


if __name__ == '__main__':
    loop_menu()
