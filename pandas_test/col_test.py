#coding=utf-8
#print data

import tensorflow as tf
import pandas as pd
import numpy as np
data =[
    [1,2,3,4,5,6,7],
    [11,21,31,41,51,61,71],
    [12,22,32,42,52,62,72],
    [13,23,33,43,53,63,73]
]
data  = np.asarray(data)
print data
i = 0
time_step =2 

print "----------------------------------"
print data[0:4,:2]
#x=data[i:i+time_step,:7]
print "----------------------------------"
#print x

print data[0:4,2,np.newaxis]
print data[0:4,2]



tensor=tf.constant(-1, shape=[2,1 ])
print tensor
a = tf.Variable(tf.random_normal([3,2]))
print a


#arr=tf.constant([[0.0,0.0,12.0],[0.0,0.0,1.0],[0.0,2.0,0.0]])
arr=tf.constant([0.0,2.0,0.0])

with tf.Session() as sess:
    print(sess.run(tf.argmax(arr, 0)))# 返回每一列的最大值的索引
    print(sess.run(tf.argmax(arr, 1)))# 返回每一行的最大值的索引

