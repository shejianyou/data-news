# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 13:12:26 2019

@author: 佘建友
"""
from selenium import webdriver

chromeOptions = webdriver.chromeOptions()
chromeOptions.add_argument('-headless')#设为无头模式
chromeOptions.add_argument('disable-infobars')#去掉提示，Chrome正收到自动测试软件的控制
chromeOptions.add_experimental_option('excludeSwitches',['enable-automation'])
browser = webdriver.Chrome(chrome_options=chromeOptions)
browser.set_page_load_timeout(4)
