# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 16:52:06 2019

@author: 佘建友
"""
import requests
import sys,json
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
N_parms_list = [
                            {'jsoncallback':'jsonp1579011048247','_':'1579011048468'},
                            {'jsoncallback':'jsonp1579011381012','_':'1579011381405'},
                            {'jsoncallback':'jsonp1579014895568','_':'1579014895701'},
                            {'jsoncallback':'jsonp1579014963161','_':'1579014963305'},
                            {'jsoncallback':'jsonp1579015145870','_':"1579015146026"},
                            {'jsoncallback':'jsonp1579015634029','_':'1579015634187'},
                            {'jsoncallback': 'jsonp1579015754609','_':'1579015754747'},
                            {'jsoncallback': 'jsonp1579015766122','_':'1579015766260'},
                            {'jsoncallback': 'jsonp1579015769963','_': '1579015770127'},
                            {'jsoncallback': 'jsonp1579015774947','_': '1579015775095'},
                            {'jsoncallback': 'jsonp1579015882803','_': '1579015882984'},
                            {'jsoncallback': 'jsonp1579015886527','_': '1579015886677'},
                            {'jsoncallback': 'jsonp1579015892360','_': '1579015892518'},
                            {'jsoncallback': 'jsonp1579015895927','_': '1579015896045'},
                            {'jsoncallback': 'jsonp1579015920516','_': '1579015920667'},
                            {'jsoncallback': 'jsonp1579015946875','_': '1579015947026'},
                            {'jsoncallback': 'jsonp1579016107416','_': '1579016107585'},
                            {'jsoncallback': 'jsonp1579016110574','_': '1579016110719'},
                            {'jsoncallback': 'jsonp1579016114572','_': '1579016114719'},
                            {'jsoncallback': 'jsonp1579016118129','_': '1579016118274'},
                            {'jsoncallback': 'jsonp1579016121338','_': '1579016121498'},
                            {'jsoncallback': 'jsonp1579016123915','_': '1579016124053'},
                            {'jsoncallback': 'jsonp1579016127366','_': '1579016127509'},
                            {'jsoncallback': 'jsonp1579016130155','_': '1579016130275'},
                            {'jsoncallback': 'jsonp1579016133594','_': '1579016133728'},
                            {'jsoncallback': 'jsonp1579016137223','_': '1579016137441'},
                            {'jsoncallback': 'jsonp1579016333761','_': '1579016333983'},
                            {'jsoncallback': 'jsonp1579016336912','_': '1579016337122'},
                            {'jsoncallback': 'jsonp1579016339499','_': '1579016339717'},
                            {'jsoncallback': 'jsonp1579016342623','_': '1579016342854'},
                            {'jsoncallback': 'jsonp1579016432551','_': '1579016432775'},
                            {'jsoncallback': 'jsonp1579016436252','_': '1579016436461'},
                            {'jsoncallback': 'jsonp1579016439083','_': '1579016439299'},
                            {'jsoncallback': 'jsonp1579016441914','_': '1579016442144'},
                            {'jsoncallback': 'jsonp1579016444896','_':'1579016445100'},
                            {'jsoncallback': 'jsonp1579016447441','_': '1579016447662'},
                            {'jsoncallback': 'jsonp1579016450252','_': '1579016450468'},
                            {'jsoncallback': 'jsonp1579016453481','_': '1579016453715'},
                            {'jsoncallback': 'jsonp1579016613342','_': '1579016613562'},
                            {'jsoncallback': 'jsonp1579016616312','_': '1579016616538'},
                            {'jsoncallback': 'jsonp1579016619221','_': '1579016619431'},
                            {'jsoncallback': 'jsonp1579016622072','_': '1579016622268'},
                            {'jsoncallback': 'jsonp1579016624790','_': '1579016625006'},
                            {'jsoncallback': 'jsonp1579016627738','_': '1579016627951'},
                            {'jsoncallback': 'jsonp1579016630184','_': '1579016630409'},
                            {'jsoncallback': 'jsonp1579016632662', '_': '1579016632880'},
                            {'jsoncallback': 'jsonp1579016634899','_': '1579016635123'},
                            {'jsoncallback': 'jsonp1579016636884','_': '1579016637101'},
                            {'jsoncallback': 'jsonp1579016639530','_': '1579016639742'},
                            {'jsoncallback': 'jsonp1579016641911','_': '1579016642132'},
                            {'jsoncallback': 'jsonp1579016646767','_': '1579016646995'},
                            {'jsoncallback': 'jsonp1579016649426','_': '1579016649626'},
                            {'jsoncallback': 'jsonp1579016652238','_': '1579016652460'},
                            {'jsoncallback': 'jsonp1579016654884','_': '1579016655114'},
                            {'jsoncallback': 'jsonp1579016657985','_': '1579016658211'},
                            {'jsoncallback': 'jsonp1579016661258','_': '1579016661470'},
                            {'jsoncallback': 'jsonp1579016663985','_': '1579016664204'},
                            {'jsoncallback': 'jsonp1579016666725','_': '1579016666945'},
                            {'jsoncallback': 'jsonp1579016669093','_': '1579016669310'},
                            {'jsoncallback': 'jsonp1579016671998','_': '1579016672196'},
                            {'jsoncallback': 'jsonp1579016674510','_': '1579016674750'},
                            {'jsoncallback': 'jsonp1579016677024','_': '1579016677233'},
                            {'jsoncallback': 'jsonp1579016679478','_': '1579016679698'},
                            {'jsoncallback': 'jsonp1579016682035','_': '1579016682254'}     
                                       ]

def parse_html(url):
    struct = {}
    r_text = requests.get(url,headers=headers)
    r_text = r_text.text
    try:
        try: #try parsing to dict
            dataform = str(r_text).replace('updatepage','')
            dataform = dataform.replace('(', '')
            dataform = dataform.replace(')','')
            struct = json.loads(dataform)
        except:
            print(repr(r_text))
            print(sys.exc_info())
        
    except:
        pass
    response = struct.get('response')
    docs = response.get('docs')
    for i in docs:
        title = i.get('title')
        print('已抓到',title)
        body = i.get('content')
        abstract = i.get('infosummary')
        author = i.get('agentname')
        url = 'https' + i.get('htmlurl')
        yield {'title':title,
                       'body':body,
                       'author':author,
                       'url':url,
                       'body':body,
                       'abstract':abstract}
    

def save_to_text(infor):
    """
    Parameters
    ----------
    infor : str
    Returns
    -------
    None.

    """
    with open(r'C:\Users\23909\Desktop\女劳模——中工网.txt','a',encoding='utf-8') as f:
        f.write(infor)
        f.write('\n')
    f.close()
        
    
if __name__ == '__main__':
    """
    it is the access of my program
    Returns
    -------
    None.
    """
    start = 0
    page = 0
    for i in N_parms_list:
        jsoncallback = i.get('jsoncallback')
        _ = i.get('_')
        url = 'http://search.workercn.cn/searchservice/info/select?start={0}&rows=10&q=%E5%A5%B3%E5%8A%B3%E6%A8%A1&q_show=%E5%A5%B3%E5%8A%B3%E6%A8%A1&sort=releasetime%20desc&wt=json&indent=on&fl=*,score&hl=true&hl.fragsize=300&hl.fl=title,content&json.wrf=updatepage&jsoncallback={1}&_={2}'.format(start, jsoncallback,_)
        start += 10
        print('\n','--'*25,'正在抓取第{0}页的信息'.format(page),'--'*25)
        items = parse_html(url)
        print('\n','--'*25,'正在存储第{0}页的信息'.format(page),'--'*25)
        for item in items:
            item = str(item)
            save_to_text(item)
        page += 1
        time.sleep(3)
        
        
        

    
    
