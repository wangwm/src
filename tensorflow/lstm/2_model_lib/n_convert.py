#coding:utf-8
import sys
import os 



import pandas as pd
import talib 
import numpy as np
#from numpy import *
#import matplotlib.pyplot as plt
#import my_tf_stock_lib.tf_backward as tfLib
import myscipy.mylib as myScipy
import time
import traceback
myScipy = myScipy.my_scipy()

ZERO_FLOAT = 0.00000001

NEW_DATA_PATH = "../../2_data_c"
PRE_NUM =65

#目前分类： WIN_RATE_LIMIT 为界限，二分类。盈利为1，数据读取时候请转成[1,0]形式，相反 低于WIN_RATE_LIMIT，则是[0,1]
#WIN_RATE_LIMIT = 0.035
WIN_RATE_LIMIT = 0.08
LOSS_RATE_LIMIT = -0.04


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
    #print new2    
    size =  len(new2)
    for index, row in new2.iterrows():
        if index >= size-1:
            break;
        if  float(new2['change'][index+1]) > WIN_RATE_LIMIT:

            new2['label'][index] =1
        else: 
            new2['label'][index] =0
        
    return  new2

 
def get_bias(close,period =6):
    
    EMA_v = talib.EMA(np.array(close), timeperiod=period) 
    bias = float(ZERO_FLOAT)
    nowprice =  close[-1]
    if EMA_v[-1] >ZERO_FLOAT:
        bias =  float(100*(close[-1] - EMA_v[-1])/EMA_v[-1])
    else:
        bias =0
    return bias    

######################
def convert2(DataFrame):
    #print DataFrame
    #样本太小不计算了
    if len(DataFrame) < 500:
        return None
    new = DataFrame[[ 'code','date','open','high','low','close','change','volume','money','turnover','adjust_price_f' ]] 
    new2 = pd.DataFrame(new, columns=['code','date','open','high','low','close','change','volume','money','turnover','linear_k60','linear_k60_loss','linear_k20','linear_k20_loss','bias','atr','label_1','label_2' ])
    
    
    #用已有数据复权全部数据，前复权
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
    new2['linear_k20'] =0 
    new2['linear_k20_loss'] =0 
    
    new2['bias'] =0  #乖离，偏离度
    new2['atr'] =0   #波动率
    new2['label_1'] =0   
    new2['label_2'] =0   
    for index, row in new2.iterrows():
        #print row["date"],index
        if index < PRE_NUM:
            continue
        #close = new2['close'][index-PRE_NUM:index]
        #high = new2['high'][index-PRE_NUM:index]
        #low = new2['low'][index-PRE_NUM:index]
        
        close = new2['close'][index-PRE_NUM+1:index+1]
        high = new2['high'][index-PRE_NUM+1:index+1]
        low = new2['low'][index-PRE_NUM+1:index+1]
        
        ma_close = talib.SMA(np.array(close), timeperiod=5)
        ma60 = ma_close[5:]  #get pre 60 day
        ma20 =ma_close[-20:]  # get pre 20day
        #print close,len(close)
        #print new2.iloc[index,0],new2.iloc[index,1],new2.iloc[index,5]
        
        #a=b
        #print ma20,len(ma20)
        #linear_k60,loss = tfLib.tf_stock_backward(ma60)
        linear_k60,loss60 = myScipy.linear_line2(ma60)
        linear_k20,loss20 = myScipy.linear_line2(ma20)
        #print linear_k60,loss60
        #print linear_k60[0],loss60[0]
        #print linear_k20[0],loss20[0]
      
        #暂时取6天为周期
        bias = get_bias(np.array(close),6)  
        
        #暂时取14天为周期
        atr = talib.ATR(np.array(high),np.array(low),np.array(close),timeperiod=14)  
        #print atr
        #print atr[-1]
        #print new2.iloc[index,0] ,new2.iloc[index,1] , bias,atr[-1]
        
        new2.iloc[index,10] = linear_k60[0] 
        new2.iloc[index,11] = loss60[0] 
        new2.iloc[index,12] = linear_k20[0] 
        new2.iloc[index,13] = loss20[0] 
        
        new2.iloc[index,14] = bias
        new2.iloc[index,15] = atr[-1]
        
        #if index % 100 ==0:
        #    print index 
            
    ####################################################################        
    #开始设定lable
    size =  len(new2)
    #寻找未来5天交易日（一周）内的最高，最低
    for index, row in new2.iterrows():
        if index >= size-6:
            break;
        min_low = np.min(new2['low'][index+1:index+6])
        max_high = np.max(new2['high'][index+1:index+6])
        nowClose = new2.iloc[index,5]
        #print nowClose,min_low,max_high
        
        varH = ZERO_FLOAT
        varL = ZERO_FLOAT
        if nowClose >ZERO_FLOAT:#close为0 暂不特殊处理，按照统一处理。估计此类样本数不多
            varH = float((max_high- nowClose)/nowClose)
            varL = float((min_low- nowClose)/nowClose)
        
        #print new2.iloc[index,0] ,new2.iloc[index,1], np.round(varH,3), np.round(varL,3)    
        new2.iloc[index,16] = varH       
        new2.iloc[index,17] = varL
        
        
    return  new2

def convertFile(filepath,descpath):
    #print filepath
    dat = pd.read_csv(filepath)
    new = convert2(dat) 
    if new is None:
        return 
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
            time.sleep(1)   
        # 遍历所有的文件夹                                        
        #for d in dirs:                                    
        #    print(os.path.join(root, d))                  
        


if __name__ == '__main__':
    #wine = pd.read_csv("sz002464.csv")
    #wine.head()
    #print "----------------------------"
    #convert(wine.head(178).tail(5))
    try:
        walkFile("./raw_data")
    except Exception,e:   
        traceback.print_exc()
