#coding=utf-8
'''
Created on 2017年2月20日
@author: Lu.yipiao
'''
import pandas as pd
import numpy as np
import tensorflow as tf

#定义常量
rnn_unit=10       #hidden layer units
input_size=7
output_size=1
lr=0.0006         #学习率
#——————————————————导入数据——————————————————————
print "bbbbbbbbbbbbbbbbbbbbbb"
f=open('test.csv') 
df=pd.read_csv(f)     #读入股票数据
data=df.iloc[:,2:10].values  #取第3-10列

print data
#获取训练集
def get_train_data(batch_size=2,time_step=2,train_begin=0,train_end=6):
    batch_index=[]
    data_train=data[train_begin:train_end]
    print type(data_train)
    normalized_train_data=(data_train-np.mean(data_train,axis=0))/np.std(data_train,axis=0)  #标准化
    train_x,train_y=[],[]   #训练集 
    for i in range(len(normalized_train_data)-time_step):
       if i % batch_size==0:
           batch_index.append(i)
           print i
       x=normalized_train_data[i:i+time_step,:7]
       y=normalized_train_data[i:i+time_step,7,np.newaxis]
       train_x.append(x.tolist())
       train_y.append(y.tolist())
       print x.tolist(),type(train_x),type(x.tolist())
       break
    print "-----------------------------"
    batch_index.append((len(normalized_train_data)-time_step))

    print type(train_x)
    return batch_index,train_x,train_y

#get_train_data()
#
x = tf.constant(-3.0, dtype=tf.float32)
print x

x1 = tf.constant(-3.0,shape=[], dtype=tf.float32)
print x1

x2 = tf.constant(-1,shape=[4], dtype=tf.float32)
print x2
x4 = tf.constant(-1,shape=[4,], dtype=tf.float32)
print x4
x5 = tf.constant(-1,shape=[4,5], dtype=tf.float32)
print x5

v1 =  tf.get_variable("aa", [], initializer=tf.truncated_normal_initializer(stddev=0.1))
print v1 

v2 =  tf.get_variable("aa2", [2], initializer=tf.truncated_normal_initializer(stddev=0.1))
print v2 
v3 =  tf.get_variable("aa3", [2,], initializer=tf.truncated_normal_initializer(stddev=0.1))
print v3 
v4 =  tf.get_variable("aa4", [2,5], initializer=tf.truncated_normal_initializer(stddev=0.1))
print v4

y = tf.placeholder(tf.float32, [None, 5], name='y-input')
print y
