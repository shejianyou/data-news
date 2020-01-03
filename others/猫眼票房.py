# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 12:26:50 2019

@author: 23909
"""
#提取首页的源代码
import json
import requests
from requests.exceptions import RequestException
import re
import time

def get_one_page(url):
    try:
        headers = {
                'User-Agent':'Mozilla/5.0(Macintosh;Intel Mac OS X 10_13_3) AppleWebKit/537.36(KHTML,like Gecko) Chrome/65.0.3325.162 Safari/537.35'
                 }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

#通过正则表达式从结果中提取我们想要的内容
def parse_one_page(html):
    pattern = re.compile(
            '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',
            re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
                'index':item[0],
                'image':item[1],
                'title':item[2].strip(),
                'actor':item[3].strip()[3:],
                'time':item[4].strip()[5:],
                'score':item[5] + item[6]
                }

#写入文件
def write_to_file(content):
    with open('result.csv','a',encoding='gbk') as f:
        print(type(json.dumps(content)))
        f.write(json.dumps(content,ensure_ascii=False) + '\n')

#整合代码
def main(offset):
    url = 'http://maoyan.com/board/4?offset= ' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i*10)
        time.sleep(1)

    

