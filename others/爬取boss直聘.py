# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 15:02:03 2019

@author: 佘建友
"""
import requests
from lxml import etree
from selenium import webdriver

def get(page,ka):
    headers ={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    url = 'https://www.zhipin.com/c101010100/?query=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&page=2&ka=page-2'
    r = requests.get(url)
    html = etree.HTML(r.text)
    with open(r'C:\Users\23909\Desktop\刺猬实习.csv','a',encoding='utf-8') as csvfile:
        job_title = html.xpath('*//h3/a/div[@class="job-title"]/text()')
        print(job_title)
    

