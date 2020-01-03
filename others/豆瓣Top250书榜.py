# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 22:49:16 2019

@author: 23909
"""
import requests
from lxml import etree
from requests.exceptions import RequestException
import time

"""
获取网页源代码
"""
def get_one_page(url):
    try:
        headers = {
        'Cookie':'bid=mkWq9Ir16x8; gr_user_id=4cca8a44-50a2-4a2b-9be9-a7f8eed989c9; _vwo_uuid_v2=D9D9C9EC3334CA4751EF4A72F0CEF8EBE|6dd31f317a919b334a42536ecacc1990; __yadk_uid=ia133B8m585nV96OfAse9wATJPWTZYWQ; ll="108288"; douban-fav-remind=1; viewed="1872091_10760444_26702568_2154713_27109832"; dbcl2="178012444:aOEzTP1kEqI"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.17801; Hm_lvt_6e5dcf7c287704f738c7febc2283cf0c=1574348816; ck=0t5J; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1574505309%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; ap_v=0,6.0; __utma=30149280.293901289.1570968970.1574428097.1574505310.14; __utmc=30149280; __utmz=30149280.1574505310.14.11.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=81379588.1209234116.1570968970.1574428097.1574505310.9; __utmc=81379588; __utmz=81379588.1574505310.9.7.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.3ac3=0707578348872bcf.1570968970.9.1574505353.1574428527.'
        ,
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return '抓取失败'
    except RequestException:
        return None

def parse_one_page(html):
    with open(r'C:\Users\23909\Desktop\豆瓣.txt','w',encoding='utf-8') as f:
        f.write(html)
    html = etree.parse(r'C:\Users\23909\Desktop\豆瓣.txt',etree.HTMLParser())
    book_name =html.xpath('//a/@title') 
    print(book_name)
    book_img =html.xpath('//img/@src')
    print(book_img)
    book_author = html.xpath('//td[@valign="top"]/p[@class="pl"]/text()')
    print(book_author)
    book_score = html.xpath('//span[@class="rating_nums"]/text()')
    print(book_score)
    book_value = html.xpath('//span[@class="inq"]/text()')
    print(book_value)
    for i in range(25):
        with open(r'C:\Users\23909\Desktop\content.txt','a',encoding='utf-8') as my:
            my.write(book_name[i]+',')
        my.close()
        with open(r'C:\Users\23909\Desktop\content.txt','a',encoding='utf-8') as my:
            my.write(book_img[i]+',')
        my.close()
        with open(r'C:\Users\23909\Desktop\content.txt','a',encoding='utf-8') as my:
            my.write(book_author[i]+',')
        my.close()
        with open(r'C:\Users\23909\Desktop\content.txt','a',encoding='utf-8') as my:
            my.write(book_score[i]+'\n')
        my.close()
def main(start):
    url = 'https://book.douban.com/top250?start='+str(start)
    html = get_one_page(url)
    parse_one_page(html)

"""
控制网页页码并触发程序
"""  
if __name__=='__main__':
    for page in range(10):
        main(start=page*25)
        time.sleep(1)
   


      
    



















