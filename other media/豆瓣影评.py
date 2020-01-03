# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 16:04:35 2019

@author: 佘建友
"""
from lxml import etree
import requests
import json
import time
headers = {
        'Referer':'https://movie.douban.com/explore',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        }
def get_mainpage(start):
    """
    :return a dict
    """
    params = {
            'type': 'movie',
            'tag': '热门',
            'sort': 'time',
            'page_limit': '20',
            'page_start': start,
            }
    print('正在抓取第',start,'页')
    time.sleep(3)
    douban_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=time&page_limit=20&page_start={0}'.format(start)
    r = requests.get(douban_url,headers=headers)
    datas = json.loads(r.text)
    items = datas.get('subjects')
    for item in items:
        yield{
        'rate':item.get('rate'),
        'title':item.get('title'),
        'url':item.get('url')
        }  
        
def get_movieinfo(url):
    """
    获取电影主演，电影类型，电影国籍，
    电影上映日期，电影片长
    :return a dict
    """
    movie_id = url.split('/')[-2]
    headers={
            'Cookie':'bid=mkWq9Ir16x8; gr_user_id=4cca8a44-50a2-4a2b-9be9-a7f8eed989c9; _vwo_uuid_v2=D9D9C9EC3334CA4751EF4A72F0CEF8EBE|6dd31f317a919b334a42536ecacc1990; ll="108288"; douban-fav-remind=1; viewed="1872091_10760444_26702568_2154713_27109832"; dbcl2="178012444:aOEzTP1kEqI"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.17801; ck=0t5J; ap_v=0,6.0; __utma=30149280.293901289.1570968970.1575563475.1575723987.17; __utmb=30149280.0.10.1575723987; __utmc=30149280; __utmz=30149280.1575723987.17.13.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; frodotk="83041fbfa6778d15890c5f3ef366a73f"',
            'Refer':'Referer: https://movie.douban.com/subject/{0}/?tag=%E7%83%AD%E9%97%A8&from=gaia'.format(movie_id),
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
            }
    url0 = 'https://m.douban.com/rexxar/api/v2/gallery/subject_feed?start=0&count=4&subject_id={}&ck=0t5J'.format(movie_id)
    response = requests.get(url0,headers=headers)
    print(response.status_code)
    try:
        if response.status_code == 200:
            info = json.loads(response.text)
            items = info.get('items')
            o = items.get('0')
            subject_card = o.get('topic')
            yield {
                    'abstract':subject_card.get('abstract')
                    }
    except:
        print('抓取失败')

def get_review(url):
    """
    return a dict
    """
    movie_id = url.split('/')[-2] 
    headers = {
            'refer':'https://movie.douban.com/subject/27119724/reviews',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        }
    for start in range(0,100,20):
        time.sleep(3)
        url_review = 'https://movie.douban.com/subject/{1}/reviews?start={0}'.format(start,movie_id)
        r_review = requests.get(url_review,headers=headers)
        try:
            if r_review.status_code == 200:
                html = etree.HTML(r_review.text,etree.HTMLParser)
                reviews = html.xpath('//div[@class="short-content"]/text()')
                yield {
                        'reviews':reviews
                        }
        except:
            print('抓取失败')
        
def save_movieinfo0(data):
    with open(r'C:\Users\23909\Desktop\豆瓣电影.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(data,ensure_ascii=False) + '\n')
              
def main():
   url = content.get('url')
   for abstract in get_movieinfo(url):
       for reviews in get_review(url):
           yield {
                   'title':content.get('title'),
                   'rate':content.get('rate'),
                   'url':content.get('url'),
                   'abstract':abstract.get('abstract'),
                   'reviews':reviews.get('reviews')
                    }

if __name__ =='__main__':
    for start in range(0,10000,20):
        for content in get_mainpage(start):
            for i in main():
                save_movieinfo0(i)
            

        
