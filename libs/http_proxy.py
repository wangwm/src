#coding=utf-8
import os
import requests
import random
import json
import traceback
import time
import  urllib
import  urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf8')

MAX_COUNT = 3
class http_proxy:
    def __init__(self):
        self.ipport ="" 
        self.proxyurl ="http://http.tiqu.qingjuhe.cn/getip?num=1&type=1&pack=51581&port=1&lb=1&pb=4&regions="
        self.proxy_list=[]

    def reload_proxy(self):
        resp = requests.get(self.proxyurl)
        self.proxy_list = resp.text.split()
        print "reload ip list ok"
        print self.proxy_list
      

        
    def get_random_ip(self):
        size = len(self.proxy_list)
        if size <=0:
            self.reload_proxy()
            size = len(self.proxy_list)
            
        if len(self.ipport) <=0:
            index = random.randint(0,size-1)
            self.ipport = self.proxy_list[index]
            
        print "getip----------------------->", self.ipport
        return self.ipport
    
    def refresh_random_ip(self):
        if len(self.ipport) >0 and len(self.proxy_list) >0:#del old
            self.proxy_list.remove(self.ipport)
        
        self.ipport = ""
        print "delete old ip----------------------->", self.ipport
        
        
    def proxy_req_http_post(self,url,obj):
        
        
        while True:
            self.get_random_ip()
            
            ar =  self.ipport.split(":")
            proxyHost=ar[0]
            proxyPort=ar[1]
            proxyMeta = "http://%(host)s:%(port)s" % {
                "host" : proxyHost,
                "port" : proxyPort,
            }
            proxies = {
                "http"  : proxyMeta,
            }
            #headers = {'Content-Type': 'application/x-www-form-urlencoded;'}
            #headers = {'content-type':'charset=utf8'}
            headers = {'User-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'};
            
            max_con = 0
            while(max_con <MAX_COUNT):
                try:    
                    
                    httpproxy_handler = urllib2.ProxyHandler(proxies)
                    opener = urllib2.build_opener(httpproxy_handler)
                    request = urllib2.Request(url,headers=headers, data=obj)
                    response = opener.open(request,timeout=10)
                    print "opeing ok"
                    res =  response.read()  
                    print "reading ok"
                    if not res:
                        max_con+=1;
                        time.sleep(1)
                        print "opening error 1"
                        continue

                    if len(res)<=200:
                        max_con+=1;
                        time.sleep(1)
                        print "opening error",max_con
                        continue
                       
                    return res
                    
                except Exception,e:
                    traceback.print_exc()
                    time.sleep(1)
                    max_con +=1
                    print "connect num=",max_con
                    continue
                    
            self.refresh_random_ip()      
            #end while(max_con >=MAX_COUNT):


    
                  
if __name__ == '__main__':
    try:	
 
        proxy = http_proxy()
               
        phone = "18618287931"
        url = "http://m.life.httpcn.com/m/sjhm/"
        #url = "http://m.life.httpcn.com/"
        url = "http://blog.chinaunix.net/uid/52437.html"
        send = "act=submit&word=%s&data_type=0&RenYue=0&year=1976&month=1&day=31&hour=7&minute=20&zty=0&sex=1&wxxymore=0&xiyong=0&isbz=1" % (phone)
        
        res = proxy.proxy_req_http_post(url,send)
        #print res
	f= open("aaa.txt","w")
	f.write(res)
	f.close()
	#print res
    except Exception as e:
        traceback.print_exc()
        
