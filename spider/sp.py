#-*- coding:utf-8 -*-

import sqlite3
import os
#import  win32crypt
import browsercookie
from win32.win32crypt import CryptUnprotectData
import urllib3
import urllib.request

import requests
from bs4 import BeautifulSoup
import traceback
import hashlib



def testCookie():
    username = os.environ.get('USERNAME')
    cookie_file = 'C:/Users/{UserName}/AppData/Local/Google/Chrome/User Data/Default/Cookies'.format(UserName=username)
    print(cookie_file)
    con = sqlite3.connect(cookie_file)
    cursor = con.cursor()
    domain ="1688"
    #sql = 'SELECT host_key, name, value, encrypted_value FROM cookies WHERE name = "xxxxx" and host_key="xxxxx";'
    sql = 'SELECT host_key, name, value, encrypted_value FROM cookies  WHERE host_key like "%{}%"'.format(domain)

    try:
        if cursor.execute(sql):
            for en_value in cursor:
                pwdHash = en_value[3]
                
                if pwdHash:
                    ret = CryptUnprotectData(pwdHash, None, None, None, 0)
                    a = bytes.decode(ret[0])
                    b = bytes.decode(ret[1])
                    print (a)
                    print (b)
    except Exception as e:
        print(e)

def getcookiefromchrome(host='.1688.com'):
    try:
        cookiepath=os.environ['LOCALAPPDATA']+r"\Google\Chrome\User Data\Default\Cookies"
        sql="select host_key,name,encrypted_value from cookies where host_key='%s'" % host
        with sqlite3.connect(cookiepath) as conn:
            cu=conn.cursor()        
            cookies={name:CryptUnprotectData(encrypted_value)[1].decode() for host_key,name,encrypted_value in cu.execute(sql).fetchall()}
            #print(cookies)
            return cookies    
    except Exception as e:
        print(e)
        return None

def fetch_page2(url,cookie):
    data = requests.get(url,cookies=cookie,verify=False).text
    print(type(data))
    print(data)
    soup = BeautifulSoup(data,'lxml',from_encoding="gbk")
    for tag in soup.find_all('a', class_='title-link'):
        print(tag.get_text())
    #print(soup)
    with open("E:\\aaaa.html", "w",encoding='gb18030') as f:
        f.write(data)
        print("ok")

    return data

def fetch_page_post(url,cookie,data):
    data = requests.post(url,cookies=cookie,verify=False,data=data)
    

    return data


#这个函数太慢。主要是urllib.request.urlopen影响，原因待查
def fetch_page(url,cookie):
    #cookie = "cna=irUsE18tNQICAXO3apEfcW8T; lid=ebusiness008; ali_apache_track=c_mid=b2b-52569880f0434|c_lid=ebusiness008|c_ms=1; hng=CN%7Czh-CN%7CCNY%7C156; UM_distinctid=1733d3c499932f-0d1fa7af89bcf1-b383f66-232800-1733d3c499a527; taklid=5122ba6821b248e59fe6c2d3eda33650; last_mid=b2b-52569880f0434; _is_show_loginId_change_block_=b2b-52569880f0434_false; _show_force_unbind_div_=b2b-52569880f0434_false; _show_sys_unbind_div_=b2b-52569880f0434_false; _show_user_unbind_div_=b2b-52569880f0434_false; __rn_alert__=false; alicnweb=touch_tb_at%3D1594510189530%7Clastlogonid%3Debusiness008; cookie2=1fac31db8b5f3665f97fb230ccda939f; t=2d6e6749dc8f6cb8050539acc6d19735; _tb_token_=368d943e8e400; cookie1=BYK0gcY9HayYozOGXOvZLqmW1KYZUL%2BlDOiUwvCKWCM%3D; cookie17=Vvz2yhNKBZQ%3D; sg=802; csg=e2b04118; unb=52569880; uc4=nk4=0%40BAGdcIaQ9m3CJH%2FifE6Vofa2mqIIZBk%3D&id4=0%40VHrAizSQ0Ld0HUO%2BVnVWNBn%2BLw%3D%3D; __cn_logon__=true; __cn_logon_id__=ebusiness008; ali_apache_tracktmp=c_w_signed=Y; _nk_=ebusiness008; _csrf_token=1594510677175; l=eBN7dc6VOjRqA38CBOfwlurza77tkIRAguPzaNbMiOCPO8WpPaTcWZlaw5t9CnGVh6VX-3W-27aDBeYBq61InxvTZisPjGDmn; isg=BDQ0ct2G120E5UOiy8GeTBLxBfKmDVj3c4HeW86VuL9OOdSD9Bwnh-mxvXHhwZBP"
    #cookie_dict = {i.split("=")[0]: i.split("=")[1] for i in cookie.split("; ")}
    cookie_dict = cookie
    #print("cookie_dict", cookie_dict)
    #opener = urllib2.build_opener()
    #opener.addheaders.append(('Cookie', cookie))
    #response = opener.open(url)
    #html = response.read()

    carr = ['='.join((i, j)) for i, j in cookie.items()]

    headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Cookie':';'.join(carr)
    }
    print (headers)
    
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    recdata = response.read()
    data = recdata.decode("GBK")
    print (type(data))
    
    with open("E:\\aaaa.html", "w") as f:
        f.write(data)
        print("ok")


BASEPATH ="E:"
def load_page(url):
    response=requests.get(url)
    data=response.content
    return data

def save_pic(url,name):
    #name_str = name.encode("latin1")
    #print(type(name_str))
    #md5 = hashlib.md5('%s' % (name_str)).hexdigest()

    m=hashlib.md5()
    m.update(name.encode(encoding='utf-8'))
    md5 = m.hexdigest()
    print(md5)
    p1=md5[0:2]
    p2=md5[6:8]

    try:
        path = "%s/%s/%s" %(BASEPATH,p1,p2)
        if not os.path.exists(path):
            os.makedirs(path)
        filename ='%s/%s.jpg' % (path,name)
        print(filename)
        img = load_page(url)
        with open(filenamessageboxme,'wb+') as f:
            f.write(img)
            print("mmmmmmmmmmmmmmmmmm")
                #print filename, name

    except Exception as e:
            traceback.print_exc()


url ="https://shop1367841322447.1688.com/page/offerlist_140370865.htm?spm=a2615.7691456.autotrace-paginator.4.a0422ea1oeivKI&tradenumFilter=false&sampleFilter=false&sellerRecommendFilter=false&videoFilter=false&mixFilter=false&privateFilter=false&mobileOfferFilter=%24mobileOfferFilter&groupFilter=false&sortType=wangpu_score&pageNum=3#search-bar"
#url = "https://www.baidu.com/"
cookie =  getcookiefromchrome(".1688.com")
print(cookie)
#print (headers["Cookie"])
#rr= fetch_page2(url,cookie)

#url ="https://detail.1688.com/offer/622307989807.html"
rr= fetch_page2(url,cookie)
#save_pic("http://cbu01.alicdn.com/img/ibank/2020/916/532/18043235619_1168542733.230x230.jpg","wwm")
#print(rr)