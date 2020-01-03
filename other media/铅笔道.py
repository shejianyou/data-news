# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 22:20:49 2019

@author: 佘建友
"""
import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }

url = 'https://api.pencilnews.cn/search/pc-list?sa-super-property=%7B%22device_id%22%3A%2216f572695ac72-081a5912ce4801-6701b35-921600-16f572695ad345%22%2C%22screen_width%22%3A1280%2C%22screen_height%22%3A720%7D&page=1&type=1&keyword=%E5%88%9B%E6%8A%95'
req = requests.get(url,headers=headers)

text = req.json()
data = json.get('data')
data = text.get('data')
article = data.get('article')
List = article.get('list')
article_list = req.json().get('data').get('article').get('list')
article_list
author = article_list.get('name')
type(article_list)
for article in article_list:
    author = article.get('name')
    title = article.get('title')
    get_time = article.get('create_at')
    session = article.get('cate_name')
    body = article.get('body')
    
a = (author,title,get_time,session,body)
a
author = author.replace(<em>, )
author = author.replace('<em>', )
author = author.replace('<em>','')
author
title = author.replace('<em>','')
title
for article in article_list:
    author = article.get('name')
    title = article.get('title')
    get_time = article.get('create_at')
    session = article.get('cate_name')
    body = article.get('body')
    
title = title.replace('<em>','')
title
title = title.replace('</em>','')
title
body = body.replace('<em>','')
body
body = body.replace('</em>','')
body
