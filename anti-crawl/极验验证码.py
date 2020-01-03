# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 14:31:10 2019

@author: 佘建友
"""
from selenium import webdriver #调入浏览器驱动接口
from selenium.common.exceptions import TimeoutException#调入异常
from selenium.webdriver.common.by import By#调入节点选择器
from selenium.webdriver.support import expected_conditions as EC#调入等待条件
from selenium.webdriver.support.wait import WebDriverWait#调入等待对象
from urllib.parse import urlencode#调入URL解析器
from urllib.parse import quote#调入URL解析器
import time

"""
1.加载chrome浏览器问题
"""
# 初始化
def init():
    # 定义为全局变量，方便其他模块使用
    global url, browser, username, password, wait
    # 登录界面的url
    url = 'https://passport.bilibili.com/login'
    chromedriver_path = 'C:/Users/machenike/Anaconda3/Scripts/chromedriver.exe'#你自己的
    # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 实例化一个chrome浏览器，并设置成窗口最大化
    browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    browser.maximize_window()
    # 用户名
    username = '2390993438'
    # 密码
    password = 'shejianyou123/'
    # 设置等待超时
    wait = WebDriverWait(browser, 20)

"""
2.裁剪验证码问题
"""
#对某元素截图
def save_pic(obj,name):
    try:
        pic_url = browser.save_screenshot('.\\bilibili.png')
        print("%s:截图成功!"%pic_url)
        
        #获取元素位置信息
        left = obj.location['x']
        top = obj.location['y']
        right = left + obj.size['width']
        bottom = top + obj.size['height']
        
        print('图:' + name)
        print('Left %s'%left)
        print('Top %s'%top)
        print('Right %s'%right)
        print('Bottom %s'%bottom)
        print('')
        
        

















