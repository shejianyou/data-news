# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 15:02:03 2019

@author: 佘建友
"""
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import etree
import re
import json
from selenium import webdriver
options = webdriver.ChromeOptions()
# 设置为开发者模式，防止被各大网站识别出来使用了Selenium
options.add_experimental_option('excludeSwitches', ['enable-automation'])
#停止加载图片
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
driver = webdriver.Chrome(options=options)
from lxml import etree


def get_urls(page):
    pages_url = 'https://www.baijingapp.com/index/ajax/get_article_list/type-0__page-{0}__id-26254'.format(page)
    driver.get(pages_url)
    driver.implicitly_wait(10)
    urls = driver.find_elements_by_class_name('article')
    get_url(urls)
    print('-'*10,'链接列表获取成功','-'*10)
    
    
def get_url(urls):  
    browser = webdriver.Chrome(options=options)
    for url in urls:
        t_url = url.get_attribute('href')
        print(t_url)
        browser.get(t_url)
        browser.implicitly_wait(5)
        title_author_time = driver.find_element_by_class_name('mod-head')
        t_a_t_list = title_author_time.split('\n')
        a_t_list = title_author_time.split('\n')[1].split('•')
        fav = browser.find_element_by_class_name('agree')
        views = browser.find_element_by_class_name('pull-right')
        bodys = browser.find_elements(By.XPATH,'//div[@id="message"]//p//span')
        f = open(r'C:\Users\23909\Desktop\body.txt','a',encoding='utf-8') 
        for body in bodys:
            f.write('body.text'+'\n')
        f.close()
        print('-'*10,'正文已被输入','-'*10)  
        attribute = yield {
            'title':t_a_t_list[0],
            'author':a_t_list[0],
            'time':t_a_t_list[1],
            'favs':fav.text,
            'views':views.text.split(' ')[2]
            }
        print('#'*10,'文章属性已被输入','#'*10)
        to_text(attribute)
        
def to_text(attribute):
        ff = open(r'C:\Users\23909\Desktop\文章属性.txt','a',encoding='utf-8')
        ff.write('attribue')
        ff.close()
        
        
def main():
    for page in range(1,10000):
        try:
            get_urls(page)
        except:
            print('='*10,'抓取失败','='*10)
            break
        


        
               
        
        
        
        
    

    

    
    
    





























