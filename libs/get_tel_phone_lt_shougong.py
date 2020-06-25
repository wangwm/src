#coding:utf-8
import os
import json 
import traceback
import itertools


import requests
from bs4 import BeautifulSoup
import time
import random
import  urllib
import  urllib2
import json


from http_proxy import http_proxy
http_proxy = http_proxy()

def get_cookie(url):
        #创建session对象
        session = requests.Session()
        
        #使用session发送post请求获取cookie
        session.post(url,data=payload)
        print(session.cookies.get_dict())
        return  session.cookies.get_dict()


def req_http_post(url,obj):
    try:
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        #req = urllib2.Request(url=url, headers=headers, data=json.dumps(obj))
        req = urllib2.Request(url=url, headers=headers, data=obj)
        res_data= urllib2.urlopen(req)
        #print res_data
        #print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        data = res_data.read()
        return data

    except Exception,e:
        print e
    return None


def req_http_get(url):
    try:
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        #req = urllib2.Request(url=url, headers=headers, data=json.dumps(obj))
        req = urllib2.Request(url=url, headers=headers)
        res_data= urllib2.urlopen(req)
        #print res_data
        #print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        data = res_data.read()
        return data

    except Exception,e:
        print e
    return None
    
		
def get_list_from_http_lt_yyt(sect_code):
    phone_sect_list=[]
    url = "http://num.10010.com/NumApp/NumberCenter/qryNum?callback=jsonp_queryMoreNums&provinceCode=17&cityCode=170&advancePayLower=0&sortType=1&goodsNet=4&searchCategory=3&qryType=02&numNet=%s&groupKey=4800286740&judgeType=1" %(sect_code)
    data= req_http_get(url)
    pos = len("jsonp_queryMoreNums(")
    data_n =  data[pos:-1]
    datadict =  json.loads(data_n)
    numArray =  datadict['numArray'];
    
    for v in numArray:
        v = str(v)
        v = v.strip(" \t\r\n")
        if len(v)!= 11:
            continue
        phone_sect_list.append(v)    
     
    return phone_sect_list
            
        
		
def get_list_from_file(file):
    phone_sect_list=[]
    for line in open(file, "r"):
        sect = line.strip(" \t\r\n")
        if not sect:
            continue
        if len (sect)<5:
            continue
        phone_sect_list.append(sect)
     
    return phone_sect_list
    
def generate_phones(sect):
    lst =[]
    base_str = "01349"
    
    '''
    base_str = [0,1, 3, 4,9]
    list2 = list(itertools.permutations(base_str, 4))  #全排列
    for v in list2:
        phone = "%s%s" % (sect,v)
        lst.append(phone)
    '''
    
    for i in itertools.product(base_str, repeat = 4):
        last = ''.join(i)
        phone = "%s%s" % (sect,last)
        lst.append(phone)
      
    return lst
def get_score(phone):

    url = "http://m.life.httpcn.com/m/sjhm/"
    #send = "act=submit&word=%s&xiyong=0&isbz=0" % (phone)
    send = "act=submit&word=%s&data_type=0&RenYue=0&year=1976&month=1&day=31&hour=7&minute=20&zty=0&sex=1&wxxymore=0&xiyong=0&isbz=1" % (phone)
    
    #res = req_http_post(url,send)
    res = http_proxy.proxy_req_http_post(url,send)
    soup = BeautifulSoup(res, 'lxml',from_encoding='utf-8')
    #print soup
    #score_list = soup.find_all('div',class_='num150')
    #print score_list.span
    score_text=0
    hexingshuli =0
    quantishuli=0 
    yjchanggua =0 
    yjduangua =0
    shuzinengliang_num =0
    wuxing= 0
    for tag in soup.find_all('div', class_='num150'):
        score_text = tag.find('span', class_='colred').get_text()  
        break
    
    for tag in soup.find_all('table', class_='hc-cha-table'):
        bref_lst = tag.find_all('td', class_='bre')
       
        hexingshuli = bref_lst[0].find('font').get_text()  
        
        quantishuli = bref_lst[1].find('font').get_text()  
        
        yjchanggua = bref_lst[2].find('font').get_text()  
        
        yjduangua = bref_lst[3].find('font').get_text()  

        shuzinengliang_num= 0
        for subtag2 in bref_lst[4].find_all('font'):
            shuzinengliang_num  = subtag2.get_text() 
            break

        
        wuxing = bref_lst[5].find('font').get_text()  

                
        break

    #print score_text,hexingshuli,quantishuli,yjchanggua,yjduangua,shuzinengliang_num,wuxing
    
    return  score_text,hexingshuli,quantishuli,yjchanggua,yjduangua,shuzinengliang_num,wuxing
      
def loop2(sect):
    #g_map={}
    #phone_sect_list= get_list_from_http_lt_yyt(sect)
    phone_sect_list= get_list_from_file("all.txt")
    file="lt_out_%s.txt" %(sect)
    f = open(file,'w')
    head="phone total_score,核心数理,全体数理,易经长卦,易经短卦,数字能量吉数,五行\n"
    f.write(head)
    for phone in phone_sect_list:
        score,bref_lst,hexingshuli,quantishuli,yjchanggua,yjduangua,wuxing = get_score(phone)

        ss = "%s %s %s %s %s %s %s %s \n" % (phone,score,bref_lst,hexingshuli,quantishuli,yjchanggua,yjduangua,wuxing )
        ss = ss.encode("utf-8")
        print ss
        f.write(ss)
        
        t = random.randint(1,10)
        if t ==2:
            time.sleep(1)
        
        #break
    f.close()   
    
def loop():
    #g_map={}
    phone_sect_list= get_list_from_file("b13.txt")
    f = open('out.txt','w')
    head="phone total_score,核心数理,全体数理,易经长卦,易经短卦,数字能量吉数,五行\n"
    f.write(head)
    for sect in phone_sect_list:
        #sect ="1300000"
        phone_list = generate_phones(sect)
     
        for phone in phone_list:
            score,bref_lst,hexingshuli,quantishuli,yjchanggua,yjduangua,wuxing = get_score(phone)
            #g_map[phone] = int(score)
            #ss = "%s %s\n" % (phone,score)
            ss = "%s %s %s %s %s %s %s %s \n" % (phone,score,bref_lst,hexingshuli,quantishuli,yjchanggua,yjduangua,wuxing )
            ss = ss.encode("utf-8")
            print ss
            f.write(ss)
            
            t = random.randint(1,10)
            if t ==2:
                time.sleep(1)
            
        #break
    f.close()   
    #d_order=sorted(g_map.items(),key=lambda x:x[1],reverse=False)       
    #data = json.dumps(obj=d_order)
    #with open('out.txt','w') as f:
    #    f.write(data)
                
if __name__ == '__main__':
    try:	
        loop2("131")	
        #loop()	
    except Exception as e:
        traceback.print_exc()
	
