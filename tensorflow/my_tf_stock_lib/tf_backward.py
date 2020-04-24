#coding:utf-8
#0导入模块 ，生成模拟数据集
import tensorflow as tf
import numpy as np
#import matplotlib.pyplot as plt
import tf_generateds
import tf_forward

STEPS = 5000
BATCH_SIZE = 16 
LEARNING_RATE_BASE = 0.001
LEARNING_RATE_DECAY = 0.999
REGULARIZER = 0.01



#股票数据线性回归分析，返回斜率w 和损失函数值。
#目标 通过斜率和损失值 判断股票是否横盘
#一维（1列）
def tf_stock_backward(data):
	tf.reset_default_graph()
	#x = tf.placeholder(tf.float32, shape=(None, 2))
	x = tf.placeholder(tf.float32, shape=(None, 1))#一维（1列）
	y_ = tf.placeholder(tf.float32, shape=(None, 1))

	X, Y_ = tf_generateds.stock_generateds(data)
	total_num = len(data)

	y = tf_forward.stock_forward(x, REGULARIZER)
	
	global_step = tf.Variable(0,trainable=False)	

	learning_rate = tf.train.exponential_decay(
		LEARNING_RATE_BASE,
		global_step,
		total_num/BATCH_SIZE,
		LEARNING_RATE_DECAY,
		staircase=True)


	#定义损失函数
	loss_mse = tf.reduce_mean(tf.square(y-y_))
	loss_total = loss_mse + tf.add_n(tf.get_collection('losses'))
	
	#定义反向传播方法：包含正则化
	train_step = tf.train.AdamOptimizer(learning_rate).minimize(loss_total)

	with tf.Session() as sess:
		init_op = tf.global_variables_initializer()
		sess.run(init_op)
		for i in range(STEPS):
			start = (i*BATCH_SIZE) % total_num 
			end = start + BATCH_SIZE
			sess.run(train_step, feed_dict={x: X[start:end], y_:Y_[start:end]})
			'''
			if i % 2000 == 0:
				loss_v = sess.run(loss_total, feed_dict={x:X,y_:Y_})
				print("After %d steps, loss is: %f" %(i, loss_v))
				print "w=",sess.run(tf.get_collection('wwm_line_w'))
			'''	
		loss_v = sess.run(loss_total, feed_dict={x:X,y_:Y_})
		w  = sess.run(tf.get_collection('wwm_line_w'))
		
		sess.close()		
	return w[0][0][0] ,loss_v


if __name__=='__main__':

	ttt = np.array([10.76,10.52,10.43,10.61,10.21,10.5,10.29,10.21,9.81,9.71,9.9,10.13,9.88,9.66,9.84,9.96,10.26,9.92,9.86,9.51,9.28,9.56,9.92,9.93,9.85,9.88,9.94,9.76,9.78,9.77,9.98,10.64,10.29,10.19,10.2,9.89,9.96,10.12,10.01,9.83,9.55,9.23,8.31,8.78,8.92,9.21,9.46,9.98,9.98,9.89,9.92,9.9,10.03,10.09,10.55,10.23,10.13,10.34,10.86,11.95,12.66,13.93,13.77,13.91])
        
        print "-------------------------"
        w,loss = tf_stock_backward(ttt)
        print w[0][0][0]
        print loss
        
        
	ttt = np.array([88.70613305613305,89.23172557172558,87.35744282744284,86.78226611226611,85.31457380457381,83.90638253638252,83.80721413721413,82.77586278586278,83.80721413721413,83.64854469854468,85.78066528066527,84.30305613305615,84.33280665280667,85.59224532224532,86.7326819126819,87.71444906444907,87.20869022869022,87.00043659043659,87.24835758835759,89.14247401247401,86.77234927234927,86.95085239085239,86.17733887733888,85.97900207900209,86.59384615384614,87.76403326403327,87.51611226611227,88.3,89.23,90.7,90.4,89.44,89.56,92.34,91.35,89.52,90.0,89.6,89.85,88.91,88.95,88.78,88.35,88.3,87.04,88.0,88.18,88.5,89.9,90.45,90.2,90.58,91.72,89.75,90.07,90.29,89.5,89.8,88.0,88.64,88.2,87.95,88.12,90.04])
 
        print "-------------------------"
        w,loss = tf_stock_backward(ttt)
        print w[0][0][0]
        print loss

	
        print "-------------------------"
        ttt = np.array([20.3,20.52,20.27,20.21,19.75,19.48,18.32,18.59,18.64,18.5,18.78,18.47,18.64,18.88,18.65,19.59,20.05,19.72,20.03,19.6,19.17,19.58,19.63,20.29,19.48,20.06,20.01,20.33,21.45,21.2,21.96,21.6,21.07,21.24,21.87,21.27,21.34,21.45,21.12,20.7,20.9,21.07,19.58,19.67,19.0,18.91,19.18,19.29,19.33,20.14,19.86,20.05,20.22,19.74,20.03,20.27,20.06,19.59,19.76,21.74,20.68,18.98,18.15,18.56])
        w,loss = tf_stock_backward(ttt)
        print w[0][0][0]
        print loss

