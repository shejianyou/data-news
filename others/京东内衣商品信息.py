# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 23:25:47 2019

@author: 佘建友
"""
import requests
from lxml import etree
from urllib.parse import urlencode

"""
when using the for loop,the link of every item in every page is getted,
which is contained by a list.
"""
def get_url(page,s):
    
    headers = {
            'authority': 'search.jd.com',
            'method': 'GET',
            'path': '/Search?keyword=%E5%86%85%E8%A1%A3%E5%A5%B3&enc=utf-8&spm=2.1.0',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'shshshfpa=3dd02e8a-a105-d684-db6c-a36a501f8354-1570772499; __jdu=1570772499286381696278; unpl=V2_ZzNtbUdSFxMlCBVWKBAJVWIDFFtLVkEXJVwWBngZD1FhAEUKclRCFX0URlRnGVwUZAIZXkFcRx1FCEJkeBhcBWYDFFlEUHMlfQAoVzYZMgYJAF8QD2dAFUUJdlR%2fH10DYQAXVUpUShJ3AUZTcx5fA24zIl1EZ0MUdAlHVnoeXQJkBSIGFzlFFyYIFgQrTlUFZgMbbUNnQiV0OBA6exhdBGYCE1VDUg4VcQ5HUn0aWQ1vABtaQF5DEn0PRVJyKV01ZA%3d%3d; shshshfpb=gdfeQKkp%20Rgp3ZAiqwlANyQ%3D%3D; xtest=5659.cf6b6759; qrsc=3; user-key=413e85d4-2ecd-460a-94a2-d4b9b4b827ed; cn=1; __jdv=76161171|cn.bing.com|-|referral|-|1575177653483; PCSYCityID=CN_110000_110100_110108; areaId=1; ipLoc-djd=1-2800-2848-0; __jda=122270672.1570772499286381696278.1570772499.1575300867.1575350187.10; __jdc=122270672; shshshfp=4890794bbf6b462cf05151d787ca5c6a; rkv=V0300; 3AB9D23F7A4B3C9B=FA6GMWEN2UCDLY7WFF7PNACCA5MDMKAYBBLMPOYB4ZGGXNPQ375TPSDE5XZRDWEXIA6LICXVHWLVIN4MTXBO6HMVDQ; __jdb=122270672.5.1570772499286381696278|10.1575350187; shshshsID=58cb8c5f49babb2a648653a8002c10ae_5_1575350260778',
            'referer': 'https://search.jd.com/Search?keyword=%E5%86%85%E8%A1%A3%E5%A5%B3%E5%AD%A6%E7%94%9F&enc=utf-8&spm=2.1.0',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               }
            
    params = {
            'keyword':'内衣女',
            'enc':'utf-8',
            'qrst':'1',
            'rt':'1',
            'stop':'1',
            'spm':'2.1.0',
            'vt':'2',
            'page':page,
            's':s,
            'click':'0'
            }

    url = 'https://search.jd.com/Search?' + urlencode(params)
    response = requests.get(url,headers=headers)
    html = etree.HTML(response.text)
    Llist = ['https:'+ i for i in html.xpath('//div[@class="p-img"]/a/@href') ]
    get_item(Llist)
    

def get_item(Llist):
    from selenium import webdriver #调入浏览器驱动接口
    from selenium.common.exceptions import TimeoutException#调入异常
    global browser
    browser = webdriver.Chrome()#构造一个WebDriver对象
    for url in Llist:
        print('正在爬取第',page,'页')
        try:
            browser.get(url)
        except TimeoutException:
            browser.get(url)
        get_product()

#获取商品信息
def get_product():
    product_html = browser.page_source
    doc = etree.HTML(product_html)
    name = doc.xpath('//div[@class="sku-name"]/text()')
    price = doc.xpath('//div[@class="dd"]/span[@class="p-price"]/text()')
    size = doc.xpath('//div[@class="comment-message"]/div[@class="order-info"]/span[last()-2]/text()')
    comment = doc.xpath('//div[@class="comment-column J-comment-column"]/p[@class="comment-con"]/text()')
    """
    the data mentioned above is contained by list which is one of Python data structure
    """
        
    product = {
                'name':name,
                'price':price,
                'size':size,
                'comment':comment
                }
    print(product)
    save_to_txt(product) 

#保存到MongoDB

def save_to_txt(product):
    """
    保存至txt
    :param result:结果
    """
    product = str(product)
    try:
        with open(r'C:\Users\23909\Desktop\京东内衣.txt','a',encoding='utf-8') as f:
            f.write(product + '\n')
        
    except Exception:
        print('存储到txt失败')



"""
we use the main() function to be a trigger.
"""
def main():
    for page in (x for x in range(1,201,2)):
        s = (page-1)*30 + 1
        get_url(page,s)
        s = 0 
        

num = [27182698330,10372884991,45501861350,100003087277,56512414367,10128205499,34508607458,44814461608,100004104710,54227769817,100004102879,100004567397,61300805226,100004317665,55453903060,59814706169,3649150,100003298974,61398215740,100007759900,46178173329,44496874159,100002038151,41312633647,10753632397,1794666,61011990525,58292095644,57967674113,1026599620]  








