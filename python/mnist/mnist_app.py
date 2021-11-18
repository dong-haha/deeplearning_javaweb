# coding:utf-8
import tensorflow as tf
import mnist_forward
import mnist_backward
from PIL import Image
import numpy as np


def restore_model(testPicArr):
    with tf.Graph().as_default() as tg:  # 创建一个默认图
        x = tf.placeholder(tf.float32, [None, mnist_forward.INPUT_NODE])
        y = mnist_forward.forward(x, None)
        preValue = y  # 得到概率最大的预测值
        '''
         实现滑动平均模型，参数moving_average_decay用于控制模型的更新速度，训练过程会对每一个变量维护一个影子变量
         这个影子变量的初始值就是相应变量的初始值，每次变量更新时，影子变量随之更细
        '''
        variable_averages = tf.train.ExponentialMovingAverage(mnist_backward.moving_average_decay)
        variable_to_restore = variable_averages.variables_to_restore()
        saver = tf.train.Saver(variable_to_restore)

        with tf.Session() as sess:
            # 通过checkpoint文件定位到最新保存的模型
            ckpt = tf.train.get_checkpoint_state(mnist_backward.model_save_path)
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)

                preValue = sess.run(preValue, feed_dict={x: testPicArr})
                return preValue
            else:
                print("no checkpoint file found")
                return -1


# 预处理函数，包括resize,转变灰度图，二值化操作等
def pre_pic(picName):
    img = Image.open(picName)
    reIm = img.resize((28, 28), Image.ANTIALIAS)
    im_arr = np.array(reIm.convert('L'))
    threshold = 50  # 设定合理的阈值
    for i in range(28):
        for j in range(28):
            im_arr[i][j] = 255 - im_arr[i][j]  # 模型要求黑底白字，输入图为白底黑字，对每个像素点的值改为255-原值=互补的反色
            if (im_arr[i][j] < threshold):
                im_arr[i][j] = 0
            else:
                im_arr[i][j] = 255

    nm_arr = im_arr.reshape([1, 784])  # 1行784列
    nm_arr = nm_arr.astype(np.float32)
    img_ready = np.multiply(nm_arr, 1.0 / 255.0)  # 从0-255之间的数变为0-1之间的浮点数

    return img_ready


if __name__ == '__main__':
    testNum = int(input("input the number of test pictures:"))
    for i in range(testNum):
        testPic = input("the path of test picture:")
        testPicArr = pre_pic(testPic)
        preValue = restore_model(testPicArr)
        print("the prediction number is", preValue)
