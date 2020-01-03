# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 17:04:32 2019

@author: 佘建友
"""
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import urlencode

browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
KEYWORD = 'ipad'
headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Cookie':'thw=cn; cna=iQMnFsYfBnwCAXx/y3TQv0Um; t=958a5452684ddc41c6b605c1d6b2d4ca; lgc=%5Cu53CB%5Cu53CBgg%5Cu5374; tracknick=%5Cu53CB%5Cu53CBgg%5Cu5374; tg=0; enc=2tRzUgdYqBV1MUkE2LEQcS1Ix%2BTZmthtOvyH0tbaRLOR00HoYZEUnU1cGpzubQvH8lYsXvINwiSWIXC9yGXvJA%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; uc3=id2=UU8BpJad4tEhEQ%3D%3D&vt3=F8dByuWkzP7rPqcqSuo%3D&lg2=UtASsssmOIJ0bQ%3D%3D&nk2=sFHgbBFNknQ%3D; uc4=nk4=0%40sqnBRdQBKiB6FE1IT87SFc8mhw%3D%3D&id4=0%40U22GXuShBa%2FZDPbUfWogYVl2WMqO; _cc_=VFC%2FuZ9ajQ%3D%3D; mt=ci=-1_0; v=0; cookie2=1c38f0d42d9b908b3e39885534aa9797; _tb_token_=e307580e4f8b7; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=9C1388B52F31223E143911B6AAAC6D62; uc1=cookie14=UoTbmEnhmk5InQ%3D%3D; l=dBxtDhH7q2xtGIOBBOCwourza77OSIRAguPzaNbMi_5hY6L_ooQOkn2ukFp6VjWftD8B4dH2-se9-etkZLy06Pt-g3fPaxDc.; isg=BE5OFHGcn1rg_is9vYAmsAnSnyQaznMugVkawniXutEM2-414F9i2fSZE0cSQwrh',
        
        }
params = {
        'q':'充气娃娃',
        'imgfile':None,
        'commend':'all',
        'ssid':'s5-e',
        'search_type': 'item',
        'sourceId': 'tb.index',
        'spm': 'a21bo.2017.201856-taobao-item.1',
        'ie': 'utf8',
        'initiative_id': 'tbindexz_20170306'
        }

def index_page(page):
    """
    抓取索引页
    :param page:页码
    """
    print('正在爬取第',page,'页')
    try:
        url = 'https://s.taobao.com/search?' + urlencode(params)
        browser.get(url)
        if page > 1:
            input = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager div.form > input')))#定位输入页面按钮
            submit = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager div.form > span.btn.J_Submit')))#点击按钮
            input.clear()
            input.send_keys(page)
        wait.until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager li.item.active > span'),str(page))
                )
        wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'.m-itemlist .items .item'))
                )
        get_products()
    except TimeoutException:
        index_page(page)
        
#解析商品列表
from pyquery import PyQuery as pq
def get_products():
    """
    提取商品数据
    """
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
                'image':item.find('.pic.img').attr('data-src'),
                'price':item.find('.price').text(),
                'deal':item.find('.deal-cnt').text(),
                'title':item.find('.title').text(),
                'shop':item.find('.shop').text(),
                'location':item.find('.location').text()
                }
        print(product)
        save_to_mongo(product)
        
#保存到MongoDB
import pymongo
MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'products'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
def save_to_mongo(result):
    """
    保存到MongoDB
    :param result:结果
    """
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')
        
#遍历每页
MAX_PAGE = 100
def main():
    """
    遍历每一页
    """
    for i in range(1,MAX_PAGE+1):
        index_page(i)

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        