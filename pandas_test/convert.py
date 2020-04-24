#coding:utf-8
import sys
import os 



import pandas as pd
import talib 
import numpy as np
#from numpy import *
#import matplotlib.pyplot as plt
#import my_tf_stock_lib.tf_backward as tfLib


NEW_DATA_PATH = "../../data_c"
PRE_NUM =75
def convert(DataFrame):
    #print DataFrame
    new = DataFrame[[ 'code','date','open','high','low','close','change','volume','money','turnover','adjust_price_f' ]] 
    new2 = pd.DataFrame(new, columns=['code','date','open','high','low','close','change','volume','money','turnover'])
    #new2 = pd.DataFrame(new)
    new2["high"] = new['high'] *  new['adjust_price_f']/new['close']
    new2['high'] = new2['high'].round(2) 
    
    new2['low'] = new['low'] *  new['adjust_price_f']/new['close']
    new2['low'] = new2['low'].round(2) 
    
    new2['open'] = new['open'] *  new['adjust_price_f']/new['close']
    new2['open'] = new2['open'].round(2) 
    new2['close'] = new['adjust_price_f'].round(2)
    new2['label'] =0 
    
    #按照时间升序 
    new2 = new2.sort_values(by='date',axis=0)
    new2 = new2.reset_index(drop=True)
    print new2    
    size =  len(new2)
    for index, row in new2.iterrows():
        if index >= size-1:
            break;
        if  float(new2['change'][index+1]) > 0.035:
            new2['label'][index] =1
        else: 
            new2['label'][index] =0
        
    return  new2


######################
'''
def convert2(DataFrame):
    #print DataFrame
    new = DataFrame[[ 'code','date','open','high','low','close','change','volume','money','turnover','adjust_price_f' ]] 
    new2 = pd.DataFrame(new, columns=['code','date','open','high','low','close','change','volume','money','turnover'])
    #new2 = pd.DataFrame(new)
    new2["high"] = new['high'] *  new['adjust_price_f']/new['close']
    new2['high'] = new2['high'].round(2) 
    
    new2['low'] = new['low'] *  new['adjust_price_f']/new['close']
    new2['low'] = new2['low'].round(2) 
    
    new2['open'] = new['open'] *  new['adjust_price_f']/new['close']
    new2['open'] = new2['open'].round(2) 
    new2['close'] = new['adjust_price_f'].round(2)
    
    #按照时间升序 
    new2 = new2.sort_values(by='date',axis=0)
    new2 = new2.reset_index(drop=True)
    new2['linear_k60'] =0 
    new2['linear_k60_loss'] =0 
    #print new2[new2.index%2==0]
    
    
    print new2 
    for index, row in new2.iterrows():
        #print row["date"],index
        if index < PRE_NUM:
            continue
        #print new2['close'][index-PRE_NUM:index]
        close = new2['close'][index-PRE_NUM:index]
        ma_close = talib.SMA(np.array(close), timeperiod=5)
        ma60 = ma_close[5:]
        ma60 = ma60[:-6] #size 64a
        #linear_k60,loss = tfLib.tf_stock_backward(ma60)
        linear_k60,loss = myScipy.quadraticCurve(ma60)
        #new2[index]['linear_k60'] =linear_k60 
        #print  linear_k60 
        #print linear_k60
        #print loss
        new2['linear_k60'][index] = linear_k60[0]
        new2['linear_k60_loss'][index] =loss[0] 
        if index % 100 ==0:
            print index 
    return  new2
'''

def convertFile(filepath,descpath):
    dat = pd.read_csv(filepath)
    new = convert(dat) 
    print descpath
    new.to_csv(descpath,index=False)
    
 
def walkFile(file):                                  
    for root, dirs, files in os.walk(file):               
                                               
        # root 表示当前正在访问的文件夹路径                             
        # dirs 表示该文件夹下的子目录名list                           
        # files 表示该文件夹下的文件list                            
                                                   
        # 遍历文件                                            
        for f in files:
            srcPath = os.path.join(root, f)                  
            descPath = os.path.join(root,NEW_DATA_PATH, f)                  
            convertFile(srcPath,descPath)                                              
        # 遍历所有的文件夹                                        
        #for d in dirs:                                    
        #    print(os.path.join(root, d))                  



if __name__ == '__main__':
    #wine = pd.read_csv("sz002464.csv")
    #wine.head()
    #print "----------------------------"
    #convert(wine.head(178).tail(5))
    walkFile("./dat/RX")
