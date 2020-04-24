#coding:utf-8

import time
import tensorflow as tf

import tf_inference2 as tf_inference
import tf_train2 as tf_train
import tf_data_factroy2 as tf_data_factroy

import traceback

# #### 1. 每10秒加载一次最新的模型

# In[2]:


# 加载的时间间隔。
EVAL_INTERVAL_SECS = 1 

def get_win_ht(label_y,p_y):
    f = p_y.eval()
    for k in f:
        print f

def evaluate(test_x,test_y):
    with tf.Graph().as_default() as g:
        #x = tf.placeholder(tf.float32, [None, tf_inference.INPUT_NODE], name='x-input')
        x = tf.placeholder(tf.float32, shape=[None,tf_inference.TIME_STEP,tf_inference.INPUT_NODE], name='x-input_test')
        #y_ = tf.placeholder(tf.float32, [None, tf_inference.OUTPUT_NODE], name='y-input')
        y_ = tf.placeholder(tf.float32, shape=[None,tf_inference.TIME_STEP,tf_inference.OUTPUT_NODE],name='y-input_test')        

        validate_feed = {x: test_x, y_:test_y}
        

        
        pred_y,_ = tf_inference.inference(x, None)
 
        r_y =  tf.reshape(pred_y,[-1,2])
        r_y_ =  tf.reshape(y_,[-1,2])
        #r_y =  pred_y[-1]
        #r_y_ =  y_[-1]
        #aaa = tf.argmax(r_y_, 1)
        correct_prediction = tf.equal(tf.argmax(r_y, 1), tf.argmax(r_y_, 1))

        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        variable_averages = tf.train.ExponentialMovingAverage(tf_train.MOVING_AVERAGE_DECAY)
        variables_to_restore = variable_averages.variables_to_restore()
        saver = tf.train.Saver(variables_to_restore)

        
        with tf.Session() as sess:
            ckpt = tf.train.get_checkpoint_state(tf_train.MODEL_SAVE_PATH)
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
                global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
                #print sess.run(correct_prediction, feed_dict=validate_feed) 
                accuracy_score = sess.run(accuracy, feed_dict=validate_feed)
                print("After %s training step(s), validation accuracy = %g" % (global_step, accuracy_score))
                #p_y = sess.run(r_y, feed_dict=validate_feed)
                #get_win_ht(test_y,p_y)
            else:
                print('No checkpoint file found')
                return
    


def main(argv=None):
    
    dataobj = tf_data_factroy.generate("lstmStock_test",60)
    #dataobj = tf_data_factroy.generate("stockLsmtDatatest_win_hit",60)
    while True:
        X,Y_ = dataobj.next_test_data()
        if not X:
            break;
        evaluate(X,Y_)
        break;
        time.sleep(EVAL_INTERVAL_SECS)


if __name__ == '__main__':
    try:
        main()
    except Exception,e:   
        traceback.print_exc()

