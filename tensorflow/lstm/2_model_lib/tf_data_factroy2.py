#coding:utf-8

import pandas as pd
import numpy as np
import json
#import matplotlib.pyplot as plt
#import tensorflow as tf
import random
class MyInputException(Exception):  
    def __init__(self, name):  
        Exception.__init__(self)  
        self.name = name
#csv_file_train  ="./csv_train_test/sz000763_train.csv"        
csv_file_train  ="./csv_train_test/sz000002_train.csv"        
csv_file_test  ="./csv_train_test/sz000002_test.csv"        

#COL_NUM = 8
COL_NUM = 14

json_section_file ="./high_low_section.json"
g_section_map ={}
with open(json_section_file,'r')as f:
    strText = f.read()
    g_section_map = json.loads(strText)

def get_vector_by_label(data):
    out =[]
          
    for v in data:
        label = v[1]
        code = v[0]
        #print v
        #print code,label
        
        if not g_section_map.has_key(code):
            continue
        stock_section = g_section_map[code]['high']   #只是取出5一天内最大涨幅 
        
        #print stock_section
        item =[0,0,0,0,0]#五个分类
        if label < stock_section[0]['maxk']:
            item[0] = 1
        elif label >= stock_section[1]['mink']  and label < stock_section[1]['maxk']:
            item[1] = 1
        elif label >= stock_section[2]['mink']  and label < stock_section[2]['maxk']: 
            item[2] = 1
        elif label >= stock_section[3]['mink']  and label < stock_section[3]['maxk']: 
            item[3] = 1
        elif label >= stock_section[3]['mink']:
            item[4] = 1  
        #print item
        
        out.append(item)    
    out =np.array(out)   
    return out
    
    
    
class stockLsmtDatatest_win_hit:
    def __init__(self,name,time_step=20,train_begin=0,train_end=5800):
        self.__name=name
        self.INPUT_COL_NUM = COL_NUM  #7列特征向量
        self.time_step=time_step
        self.train_begin=train_begin;
        self.train_end=train_end;

        self.train_x =[]   #训练集 list
        self.train_y=[]    #label集合
        self.total_num =  0
        self.current_index_step  =0;

        f=open(csv_file_test) 
        df=pd.read_csv(f)     #读入股票数据
        df =df[:-5]
        data=df.iloc[:,2:16].values  #取第3-16列,data为array类型
        #data_label=df.iloc[:,16:18].values
        data_label = df.iloc[:,[0,16,17]].values
        data_y=get_vector_by_label(data_label)     
        print len(data_label),len(data_y),len(data)
        if len(data_y )!=len(data_label):
            raise MyInputException("数据不一致")
        train_end = len(data) 
        
        data_train=data[train_begin:train_end]
        data_train_y=data_y[train_begin:train_end]
        
        #标准化
        normalized_train_data=(data_train-np.mean(data_train,axis=0))/np.std(data_train,axis=0)  
        print len(df),len(normalized_train_data),len(data_train),len(data_train_y)
        for i in range(len(normalized_train_data)):
            if i <self.time_step:
                continue
                
            #if df.iloc[i-1,10] == 0:
            #    continue;
            #print   df.iloc[i-1,0],df.iloc[i-1,1],df.iloc[i-1,10]
            #print   df.iloc[i-1,2],df.iloc[i-1,3]
            #print    data_train[i-1][0],data_train[i-1][1]
            #print    data_train[i-self.time_step:i,:self.INPUT_COL_NUM]
            
            #训练输入，取time_step行，INPUT_COL_NUM列
            x=normalized_train_data[i-self.time_step:i,:self.INPUT_COL_NUM]
            
            
            #label，#取time_step行，1列 。注意下面仅仅是取一列。
            y=data_train_y[i-self.time_step:i]
            #array 转换到python 内置list。一个time_step行，INPUT_COL_NUM列二维（list）， 压入（list）train_x
            self.train_x.append(x.tolist()) 
            #array 转换到python 内置list。一个time_step行，1列二维（list）， 压入（list）train_y
            self.train_y.append(y.tolist()) 
        self.total_num = len(self.train_x)
        print "aaaaaaaaaaaaaaaaaaaaa"
    
    
    def next_test_data(self):
        if (self.total_num < 1):
            return None,None
        index = self.current_index_step ;
        self.current_index_step += 1;
        #return self.train_x[index],self.train_y[index]
        #print self.train_y[index:index+1]
        #return self.train_x[index:index+1],self.train_y[index:index+1]
        return self.train_x[index:index+self.total_num],self.train_y[index:index+self.total_num]


        
        

class stockLsmtDatatest:
    def __init__(self,name,time_step=20,train_begin=0,train_end=5800):
        self.__name=name
        self.INPUT_COL_NUM = COL_NUM  #7列特征向量
        self.time_step=time_step
        self.train_begin=train_begin;
        self.train_end=train_end;

        self.train_x =[]   #训练集 list
        self.train_y=[]    #label集合
        self.total_num =  0
        self.current_index_step  =0;

        f=open(csv_file_test) 
        df=pd.read_csv(f)     #读入股票数据
       
        df =df[:-5]
        data=df.iloc[:,2:16].values  #取第3-16列,data为array类型
        #data_label=df.iloc[:,16:18].values
        data_label = df.iloc[:,[0,16,17]].values
        data_y=get_vector_by_label(data_label)     
        print len(data_label),len(data_y),len(data)
        if len(data_y )!=len(data_label):
            raise MyInputException("数据不一致")
        
        #按照实际行数。若文件过大，逐行读取时候要改
        train_end = len(data) 
        
        data_train=data[train_begin:train_end]
        data_train_y=data_y[train_begin:train_end]
        #标准化
        normalized_train_data=(data_train-np.mean(data_train,axis=0))/np.std(data_train,axis=0)  

        for i in range(len(normalized_train_data) - self.time_step):
            #训练输入，取time_step行，INPUT_COL_NUM列
            x=normalized_train_data[i:i+self.time_step,:self.INPUT_COL_NUM]
            #label，#取time_step行，1列 。注意下面仅仅是取一列。
            y=data_train_y[i:i+self.time_step]
            #array 转换到python 内置list。一个time_step行，INPUT_COL_NUM列二维（list）， 压入（list）train_x
            self.train_x.append(x.tolist()) 
            #array 转换到python 内置list。一个time_step行，1列二维（list）， 压入（list）train_y
            self.train_y.append(y.tolist()) 
            
        self.total_num = len(self.train_x)
       
    
    
    def next_test_data(self):
        if (self.total_num < 1):
            return None,None
        index = self.current_index_step ;
        self.current_index_step += 1;
        #return self.train_x[index],self.train_y[index]
        #print self.train_y[index:index+1]
        #return self.train_x[index:index+1],self.train_y[index:index+1]
        return self.train_x[index:index+self.total_num],self.train_y[index:index+self.total_num]


class stockLsmtData:
    def __init__(self,name,batch_size=60,time_step=20,train_begin=0,train_end=5800):
        self.__name=name
        self.INPUT_COL_NUM = COL_NUM  #7列特征向量
          
        self.total_batch_nums = 0;
        self.batch_size=batch_size;
        self.time_step=time_step
        self.train_begin=train_begin;
        self.train_end=train_end;
        
        self.train_x =[]   #训练集 list
        self.train_y=[]    #label集合
        self.batch_index =[]
        self.current_batch_index_step  = 0
        
        
        f=open(csv_file_train) 
        df=pd.read_csv(f)     #读入股票数据
        
        df = df[65:]
        
    #增加label第二个维度;目标构造二维向量 [1,0] [0,1] 形式
        
        data=df.iloc[:,2:16].values  #取第3-16列,data为array类型
        #data_label=df.iloc[:,16:18].values
        data_label = df.iloc[:,[0,16,17]].values
        data_y=get_vector_by_label(data_label)     
        print len(data_label),len(data_y),len(data)
        if len(data_y )!=len(data_label):
            raise MyInputException("数据不一致")
        
        
        #按照实际行数。若文件过大，逐行读取时候要改
        train_end = len(data) 
        
        data_train=data[train_begin:train_end]
        data_train_y=data_y[train_begin:train_end]
        #标准化
        normalized_train_data=(data_train-np.mean(data_train,axis=0))/np.std(data_train,axis=0)  
        
        #数据输入和标记lable都在同一行。注意range使用range（10） ：0-9
        #for i in range(len(normalized_train_data) - self.time_step):
        for i in range(len(normalized_train_data) - self.time_step + 1):
            #标记batch 在原先数据中的位置，便于取出
            if i % self.batch_size==0:
                self.batch_index.append(i)
            
            #训练输入，取time_step行，INPUT_COL_NUM列
            x=normalized_train_data[i:i+self.time_step,:self.INPUT_COL_NUM]
            
                        
            #label，#取time_step行，1列 。注意下面仅仅是取一列。
            #y=normalized_train_data[i:i+self.time_step,self.INPUT_COL_NUM,np.newaxis]
            y=data_train_y[i:i+self.time_step]
            #array 转换到python 内置list。一个time_step行，INPUT_COL_NUM列二维（list）， 压入（list）train_x
            self.train_x.append(x.tolist()) 
            #array 转换到python 内置list。一个time_step行，1列二维（list）， 压入（list）train_y
            self.train_y.append(y.tolist()) 
        
        #最后一个batch 可能不是整个，去除掉。也方便 后续step+1操作
        self.total_batch_nums = len(self.batch_index) -1
    
    
    #step 表示第几次batch,self.batch_index[step]表示在self.train_x开始位置。同理step+1表示后续（结束位置）
    def next_batch(self):
        if (self.total_batch_nums < 1):
            return None,None
        self.current_batch_index_step  = self.current_batch_index_step % self.total_batch_nums;
        #step  = self.current_batch_index_step % self.total_batch_nums;
        #step  = self.current_batch_index_step ;
        step = random.randint(0,self.total_batch_nums-1) 
        #self.current_batch_index_step += 1;
        return self.train_x[self.batch_index[step]:self.batch_index[step+1]],self.train_y[self.batch_index[step]:self.batch_index[step+1]]


def generate(name,batch_size):
    if name=="lstmStock_train":
        return stockLsmtData("lstmStock_train",batch_size)
    elif name=="lstmStock_test":
        return stockLsmtDatatest("lstmStock_test")
    elif name=="stockLsmtDatatest_win_hit":
        
        return stockLsmtDatatest_win_hit("stockLsmtDatatest_win_hit")    
    else:
        raise MyInputException(name)

if __name__ == "__main__":
    
    try:
        d=generate("lstmStock_train",60)
    except MyInputException,e:
        print "input worry name "+e.name
   
