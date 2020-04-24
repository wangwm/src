#coding:utf-8
#0导入模块 ，生成模拟数据集
import tensorflow as tf

#定义神经网络的输入、参数和输出，定义前向传播过程 
def get_weight(shape, regularizer):
	#w = tf.Variable(tf.random_normal(shape), dtype=tf.float32)
	w = tf.Variable(tf.random_normal(shape,stddev = 1,seed =1), dtype=tf.float32)
	tf.add_to_collection('losses', tf.contrib.layers.l2_regularizer(regularizer)(w))
	return w

def get_bias(shape):  
	#b = tf.Variable(tf.constant(0.01, shape=shape)) 
	b = tf.Variable(tf.random_normal(shape,stddev = 1,seed =1))
	return b


def stock_forward(x, regularizer):
	
	w1 = get_weight([1,1], regularizer)	
	b1 = get_bias([1])
	if not tf.get_collection('wwm_line_w'):
		tf.add_to_collection("wwm_line_w",w1)
	else:
		print "bbbbbbbbbbbbbbbbbbbbbbbbbb"
	y = tf.matmul(x, w1) + b1 
	
	return y
