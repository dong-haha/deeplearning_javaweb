# -*- coding: UTF-8 -*-
# 作者：dong
# 时间：2021.11.16
from skimage import io,transform
import tensorflow as tf
import numpy as np


path1 = "./flower_photos/2/295.jpg"


flower_dict = {1: '玫瑰', 2: '蔷薇', 3: '海棠', 4: '蓝色妖姬', 5: '百合', 6: '郁金香',
               7: '康乃馨', 8: '风信子', 9: '紫罗兰', 10: '勿忘我', 11: '四叶草',
               12: '满天星', 13: '曼陀罗', 14: '鸢尾花', 15: '雏菊', 16: '水仙花',
               17: '樱花', 18: '薰衣草', 19: '三色堇', 20: '茉莉花', 21: '睡莲',
               22: '牵牛花', 23: '合欢花', 24: '海棠花'}

w=100
h=100
c=3

def read_one_image(path):
    img = io.imread(path)
    img = transform.resize(img,(w,h,c))
    return np.asarray(img)

with tf.Session() as sess:
    data = []
    data1 = read_one_image(path1)
    data.append(data1)

    saver = tf.train.import_meta_graph('./flower_model/model.ckpt.meta')
    saver.restore(sess,tf.train.latest_checkpoint('./flower_model/'))

    graph = tf.get_default_graph()
    x = graph.get_tensor_by_name("x:0")
    feed_dict = {x:data}

    logits = graph.get_tensor_by_name("logits_eval:0")

    classification_result = sess.run(logits,feed_dict)

    #打印出预测矩阵
    print(classification_result)
    #打印出预测矩阵每一行最大值的索引
    print(tf.argmax(classification_result,1).eval())
    #根据索引通过字典对应花的分类
    output = []
    output = tf.argmax(classification_result,1).eval()
    for i in range(len(output)):
        print("第",i+1,"朵花预测:"+flower_dict[output[i]+1])

