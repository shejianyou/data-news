# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 20:42:57 2019

@author: 23909
"""
import requests
from bs4 import BeautifulSoup

headers ={
        'Cookie':'_zap=48cdb4c2-ae55-4b7b-a7a0-bb2904defff2; d_c0="ACAnFBJLLRCPTnhAXJpH9MvnKhr950_FSpk=|1570697485"; z_c0=Mi4xSHZhaENRQUFBQUFBSUNjVUVrc3RFQmNBQUFCaEFsVk5IMEdNWGdCa3B5UjVYTzZCdjg5Q0lwbjhsTEFwYkdZNWln|1570698015|139f407d4d4c75d90226702dd55ed69801fa7398; tst=r; __utmv=51854390.100--|2=registration_date=20180523=1^3=entry_date=20180523=1; q_c1=50b3e39d959b4d4fadbd76773462c1ab|1573658058000|1570944159000; __utma=51854390.1135790501.1573466493.1573466493.1574255139.2; __utmz=51854390.1574255139.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/deerchao/activities; tgw_l7_route=e2ca88f7b4ad1bb6affd1b65f8997df3; _xsrf=56020a68-48a7-43bb-8c96-2d7af78bc4dd; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1574574490,1574598703,1574602649,1574685816; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1574686504'
        ,'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }

r = requests.get('https://www.zhihu.com/explore',headers=headers)

if r.status_code == 200:
    print('抓取成功')
else:
    print('抓取失败')
    
with open(r'C:\Users\23909\Desktop\知乎.txt','w',encoding='utf-8') as f:
    f.write(r.text)

soup = BeautifulSoup(r.text,'lxml')

with open(r'C:\Users\23909\Desktop\修正后的知乎网页源代码.txt','w',encoding='utf-8') as f:
    f.write(soup.prettify())
    
print(soup.title.string)

print(soup.a.next_sibling)

print(soup.find_all(class_="ExploreSpecialCard-contentTag"))

for i,elem in enumerate(soup.find_all(class_="ExploreSpecialCard-contentTitle")):
    print(i,elem)

for i,elem in enumerate(soup.find_all(class_="ExploreCollectionCard-contentExcerpt")):
    print(i,elem)
    
print(soup.select('.ExploreCollectionCard-contentItem.ExploreCollectionCard-contentTitle'))

for div in soup.select('div'):
    print(div.string)
    













