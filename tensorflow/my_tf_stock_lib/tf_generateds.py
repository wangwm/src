#coding:utf-8
#0导入模块 ，生成模拟数据集
import numpy as np
#import matplotlib.pyplot as plt
seed = 2 



def maxminnorm(array):
	maxcols=array.max(axis=0)
	mincols=array.min(axis=0)

	data_shape = array.shape
	data_rows = data_shape[0]
	data_cols = data_shape[1]
	t=np.empty((data_rows,data_cols))
	for i in xrange(data_cols):
      	 	t[:,i]=(array[:,i]-mincols[i])/(maxcols[i]-mincols[i])
    	return t

#for stock
SAMPLE_DATA_SIZE = 64 
def stock_generateds(data):
	row_num = data.shape[0]
	if row_num != SAMPLE_DATA_SIZE:
		print "data error"
		return 
	
	#基于seed产生随机数
	rdm = np.random.RandomState(seed)
	#随机数返回300行2列的矩阵，表示300组坐标点（x0,x1）作为输入数据集
	X = rdm.randn(row_num,1)
	for i in  range(SAMPLE_DATA_SIZE):
		 #X[i]= float(i) + rdm.rand()/10.0 -0.05
		 X[i]= i
	X= maxminnorm(X)

	#作为输入数据集的标签（正确答案）
	Y_ = rdm.randn(row_num,1)
	for i in  range(SAMPLE_DATA_SIZE):
		 Y_[i]= float(data[i])
		 #Y_[i]= float(data[i]) + rdm.rand()/10.0 -0.05

	Y_= maxminnorm(Y_)	
	return X, Y_ 

'''
if __name__=='__main__':
	a =np.array([1,2,3,4])
	X,Y_ = generateds_data(a)
	print X
	print Y_
'''
