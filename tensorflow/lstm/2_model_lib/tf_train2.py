#coding:utf-8

import tensorflow as tf
import tf_inference2 as tf_inference
import tf_data_factroy2 as tf_data_factroy
import os
import traceback
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#BATCH_SIZE = 60  
BATCH_SIZE = 128  

#学习率 
LEARNING_RATE_BASE = 0.05
LEARNING_RATE_DECAY = 0.99

#正则化系数
#REGULARIZATION_RATE = 0.0001
REGULARIZATION_RATE = 0.05

#训练轮数
#TRAINING_STEPS = 10000
TRAINING_STEPS = 10000

MOVING_AVERAGE_DECAY = 0.99

MODEL_SAVE_PATH="model/"
MODEL_NAME="mymodel"



def train_lstm(data):
    
    #输入数据
    x = tf.placeholder(tf.float32, shape=[None,tf_inference.TIME_STEP,tf_inference.INPUT_NODE], name='x-input')
    #标签数据
    y_ = tf.placeholder(tf.float32, shape=[None,tf_inference.TIME_STEP,tf_inference.OUTPUT_NODE],name='y-input')
     
    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)
    
    #调用前向传播结构
    pred_y,_ = tf_inference.inference(x, regularizer)
    
    #迭代次数
    global_step = tf.Variable(0, trainable=False)

    #滑动平均
    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
    variables_averages_op = variable_averages.apply(tf.trainable_variables())
    
    #减低2维，用于后续计算  
    pred_y_r = tf.reshape(pred_y,[-1,tf_inference.OUTPUT_NODE]) 

    y_r = tf.reshape(y_,[-1,tf_inference.OUTPUT_NODE]) 
    #用tf.nn.dynamic_rnn 返回state结果计算损失函数
    #y2_ = y_[:,-1:,:] #取TIME_STEP最后一个元素
    #y_r = tf.reshape(y2_,[-1,tf_inference.OUTPUT_NODE]) 
       
    
    correct_prediction = tf.equal(tf.argmax(pred_y_r, 1), tf.argmax(y_r, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    
    #损失函数
    #cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=pred_y_r, labels=tf.argmax(y_r, 1))
    #cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=pred_y_r, labels=y_r)
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=pred_y_r, labels=y_r)
    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    loss = cross_entropy_mean + tf.add_n(tf.get_collection('losses'))
    #指数衰减，学习率设定
    learning_rate = tf.train.exponential_decay(
        LEARNING_RATE_BASE,
        global_step, #当前迭代的次数（轮数）
        data.total_batch_nums,   #完成所有样本训练，总共的轮数
        LEARNING_RATE_DECAY,
        staircase=True)
      
    #梯度下降 优化函数
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)
    #每个bachsize 统一更新
    with tf.control_dependencies([train_step, variables_averages_op]):
        train_op = tf.no_op(name='train')

    #声明存储模型参数
    saver = tf.train.Saver()
    with tf.Session() as sess:
        init_op=tf.global_variables_initializer()
        sess.run(init_op)
        
        ckpt = tf.train.get_checkpoint_state(MODEL_SAVE_PATH)
        if ckpt and ckpt.model_checkpoint_path:
           saver.restore(sess, ckpt.model_checkpoint_path)
               
       
        for i in range(TRAINING_STEPS):
            xs, ys = data.next_batch()
            #print sess.run(pred_y, feed_dict={x: xs, y_: ys})
            #print sess.run(y_r, feed_dict={x: xs, y_: ys})
             
            _, loss_value, step,accuracy_score = sess.run([train_op, loss, global_step,accuracy], feed_dict={x: xs, y_: ys})
            if i % 10 == 0:
                print("After %d training step(s), loss on training batch is %g. accuracy is %g" % (step, loss_value,accuracy_score))
                saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=global_step)

'''
                
def train(data):
    
    #输入数据
    x = tf.placeholder(tf.float32, [None, tf_inference.INPUT_NODE], name='x-input')
    
    #标签数据
    y_ = tf.placeholder(tf.float32, [None, tf_inference.OUTPUT_NODE], name='y-input')

    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)
    
    #调用前向传播结构
    y = tf_inference.inference(x, regularizer)
    
    #迭代次数
    global_step = tf.Variable(0, trainable=False)

    #滑动平均
    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
    variables_averages_op = variable_averages.apply(tf.trainable_variables())
    
    #损失函数
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(y, tf.argmax(y_, 1))
    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    loss = cross_entropy_mean + tf.add_n(tf.get_collection('losses'))
    
    #指数衰减，学习率设定
    learning_rate = tf.train.exponential_decay(
        LEARNING_RATE_BASE,
        global_step, #当前迭代的次数（轮数）
        data.total_batch_nums ,  #完成所有样本训练，总共的轮数
        LEARNING_RATE_DECAY,
        staircase=True)
      
    #梯度下降 优化函数
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)
    
    #每个bachsize 统一更新
    with tf.control_dependencies([train_step, variables_averages_op]):
        train_op = tf.no_op(name='train')

    #声明存储模型参数
    saver = tf.train.Saver()
    with tf.Session() as sess:
        ckpt = tf.train.get_checkpoint_state(MODEL_SAVE_PATH)
        if ckpt and ckpt.model_checkpoint_path:
               saver.restore(sess, ckpt.model_checkpoint_path)
        else:
               tf.global_variables_initializer().run()
        tf.global_variables_initializer().run()
        for i in range(TRAINING_STEPS):
            xs, ys = data.next_batch()
            _, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x: xs, y_: ys})
            if i % 1000 == 0:
                print("After %d training step(s), loss on training batch is %g." % (step, loss_value))
                saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=global_step)

'''



def main(argv=None):
    try:
        dataobj = tf_data_factroy.generate("lstmStock_train",BATCH_SIZE)
        #train(dataobj)
        train_lstm(dataobj)
    except Exception,e:
        traceback.print_exc()

if __name__ == '__main__':
    tf.app.run()


