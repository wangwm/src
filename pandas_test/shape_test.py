#coding=utf-8

import tensorflow as tf
a = [
[
[1,2]],
[[3,4]
],

[
[1,2]],
[[3,4]
]
]
print a
print tf.reshape(a,[-1,1])
print tf.reshape(a,[1,-1])
print tf.reshape(a,[-1])


