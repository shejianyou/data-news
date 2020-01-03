"""
Created on Sun Dec  8 16:52:23 2019

@author: 佘建友
"""
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from PIL import Image
from io import BytesIO
import time
from lxml import etree

driver = webdriver.Chrome()
articleList_url = 'https://article-api.huxiu.com/web/article/articleList'
main_url = 'https://www.huxiu.com/article/'



#获取每个文章链接
def get_LList():
    for i in range(1,1137):
        driver.get(main_url)
        time.sleep(10)
        driver.page_source
        articles = driver.find_elements_by_xpath('//div/div[@class="article-items"]/div/a')
        article_list = []
        for article in articles:
            link = article.get_attribute('href')
            article_list.append(link)
    import requests
    #解析每个文章链接
    headers ={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36' 
        }
    for i in article_list:
        response = requests.get(i,headers=headers)
        if response.status_code == 200:
            a = response.text
            with open(r'C:\Users\23909\Desktop\虎嗅.txt','w',encoding='utf-8') as f:
                f.write(response.text)
            html = etree.parse(r'C:\Users\23909\Desktop\虎嗅.txt',etree.HTMLParser())
            article_title = html.xpath('//h1[@class="author-info_username"]/text()')[0]
            article_where = html.xpath('//span[@class="author-info__username"]/text()')[0]
            article_time = html.xpath('//span[@class="article__time"]/text()')[0]
            article_text = html.xpath('//div[@class="article__content"]/p/text()')
        

        
    

    
    
    
    
    




















