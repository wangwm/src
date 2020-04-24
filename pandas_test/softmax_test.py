#coding=utf-8

import tensorflow as tf
logits=tf.constant([[1.0,2.0,3.0],[1.0,2.0,3.0],[1.0,2.0,3.0]])

#step1:do softmax
y=tf.nn.softmax(logits)

#true label
y_=tf.constant([[0.0,0.0,1.0],[0.0,0.0,1.0],[0.0,2.0,0.0]])

argmax_v =  tf.argmax(y_,1)

#step2: do cross_entropy
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
#do cross_entropy just one step
cross_entropy2=tf.nn.softmax_cross_entropy_with_logits(labels = y_, logits=logits)

cross_entropy3=tf.nn.sparse_softmax_cross_entropy_with_logits(labels = tf.argmax(y_,1), logits=logits)
#cross_entropy3=tf.reduce_sum(tf.nn.sparse_softmax_cross_entropy_with_logits(labels = tf.argmax(y_,1), logits=logits))#dont forget tf.reduce_sum()!!


with tf.Session() as sess:
    print("\nargmax result=")
    print argmax_v.eval()


    print("\nstep1:softmax result=")
    softmax=sess.run(y)
    print(softmax)

    
    print("\ncross_entropy result=")
    c_e = sess.run(cross_entropy)
    print c_e

    print("\nFunction(softmax_cross_entropy_with_logits) result=")
    c_e2 = sess.run(cross_entropy2)
    print c_e2

    print("\nFunction(sparse_softmax_cross_entropy_with_logits) result=")
    c_e3 = sess.run(cross_entropy3)
    print(c_e3)
