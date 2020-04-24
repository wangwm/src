#coding:utf-8
#定义神经网络结构，前向传播

import tensorflow as tf

#输入：
#输入层特征个数
#INPUT_NODE = 8 
INPUT_NODE = 14 
#输入层 序列个数 和INPUT_NODE 组合一个输入
TIME_STEP = 20 

#LSTM 层hiden units 表示神经元的个数
LSTM_NODE = 500  

#输出二分类   >=3% 是1；<3%是0
OUTPUT_NODE = 5


#若不使用正则化，可传递None. 预测和评估时候不用
def get_weight_variable(name,shape, regularizer):
    weights = tf.get_variable(name, shape, initializer=tf.truncated_normal_initializer(stddev=0.1))
    if regularizer != None:
        tf.add_to_collection('losses', regularizer(weights))
    return weights
    
    
 #前向传播。具体网络结构修改即可
def inference(X, regularizer):
    #tf.variable_scope 声明参数作用域 
    #tf.shape 返回变量或占位符 shape，比如3*2矩阵返回[3,2],2*4*5矩阵返回[2,4,5]
    batch_size=tf.shape(X)[0]
   # print batch_size
    time_step=tf.shape(X)[1]
   
    #输入层参数INPUT_NODE*LSTM_NODE 矩阵，带损失函数
    w_in = get_weight_variable("weights",[INPUT_NODE, LSTM_NODE], regularizer)
    b_in = tf.get_variable("biases", [LSTM_NODE,], initializer=tf.constant_initializer(0.0))
    
    #需要将tensor转成2维进行计算，计算后的结果作为隐藏层的输入。-1表示多个不确定
    input=tf.reshape(X,[-1,INPUT_NODE])  
    input_rnn=tf.matmul(input,w_in) + b_in  #tf.matmul矩阵相乘。就是一个线性方程组。各特征，用列向量表示比较合适。
    
    #将tensor转成3维，作为lstm cell的输入
    input_rnn=tf.reshape(input_rnn,[-1,time_step,LSTM_NODE]) 
    
    cell=tf.nn.rnn_cell.BasicLSTMCell(LSTM_NODE)
    #注意参数是batch_size
    init_state=cell.zero_state(batch_size,dtype=tf.float32)
    #output_rnn是记录lstm每个输出节点的结果，final_states是最后一个cell的结果
    #这个地方 返回是[batch_size,time_step,LSTM_NODE] batch_size不一定，按实际个数来。
    #此处应该取最后一个。也就是output_rnn[-1],即[time_step,LSTM_NODE]。还不是很确定，需要进一步研究其他案例
    output_rnn,final_states=tf.nn.dynamic_rnn(cell, input_rnn,initial_state=init_state, dtype=tf.float32)  
    #返回所有结果   [batch_size,time_step,LSTM_NODE]
    output=tf.reshape(output_rnn,[-1,LSTM_NODE]) 
    #用final_states.h 返回。就是每个步长，最后一个结果 [batch_size,LSTM_NODE]
    #output=tf.reshape(final_states.h,[-1,LSTM_NODE]) 
    
    w_out =  get_weight_variable("out_weights",[LSTM_NODE, OUTPUT_NODE], regularizer)
    b_out = tf.get_variable("out_biases", [OUTPUT_NODE,], initializer=tf.constant_initializer(0.0))
    #pred=tf.matmul(output,w_out) + b_out
    pred=tf.nn.softmax(tf.matmul(output,w_out) + b_out)
    

    return pred,final_states


    
'''    
#若不使用正则化，可传递None. 预测和评估时候不用
def get_weight_variable(shape, regularizer):
    weights = tf.get_variable("weights", shape, initializer=tf.truncated_normal_initializer(stddev=0.1))
    if regularizer != None:
        tf.add_to_collection('losses', regularizer(weights))
    return weights
    
def get_weight_variable(shape, regularizer):
    weights = tf.get_variable("weights", shape, initializer=tf.truncated_normal_initializer(stddev=0.1))
    if regularizer != None:
        tf.add_to_collection('losses', regularizer(weights))
    return weights 

#前向传播。具体网络结构修改即可
def inference(input_tensor, regularizer):
    #tf.variable_scope 声明参数作用域 
    with tf.variable_scope('layer1'):
        weights = get_weight_variable([INPUT_NODE, LAYER1_NODE], regularizer)
        biases = tf.get_variable("biases", [LAYER1_NODE], initializer=tf.constant_initializer(0.0))
        layer1 = tf.nn.relu(tf.matmul(input_tensor, weights) + biases)

    with tf.variable_scope('layer2'):
        weights = get_weight_variable([LAYER1_NODE, OUTPUT_NODE], regularizer)
        biases = tf.get_variable("biases", [OUTPUT_NODE], initializer=tf.constant_initializer(0.0))
        layer2 = tf.matmul(layer1, weights) + biases

    return layer2
 ''' 

