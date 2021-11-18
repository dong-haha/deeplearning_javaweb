# coding:utf-8
import time
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import mnist_forward
import mnist_backward

test_interval_secs = 5  # 程序循环间隔时间5秒


def test(mnist):
    with tf.Graph().as_default() as g:  # 复现计算图
        x = tf.placeholder(tf.float32, [None, mnist_forward.INPUT_NODE])
        y_ = tf.placeholder(tf.float32, [None, mnist_forward.OUTPUT_NODE])
        y = mnist_forward.forward(x, None)

        # 实例化滑动平均的saver对象
        ema = tf.train.ExponentialMovingAverage(mnist_backward.moving_average_decay)
        ema_restore = ema.variables_to_restore()
        saver = tf.train.Saver(ema_restore)

        # 计算准确率
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        while True:
            with tf.Session() as sess:
                ckpt = tf.train.get_checkpoint_state(mnist_backward.model_save_path)  # 加载指定路径下的滑动平均
                if ckpt and ckpt.model_checkpoint_path:
                    saver.restore(sess, ckpt.model_checkpoint_path)
                    global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
                    accuracy_score = sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels})
                    print("After %s training step(s),test accuracy= %g." % (global_step, accuracy_score))
                else:
                    print('No checkpoint file found')
                    return
            time.sleep(test_interval_secs)


if __name__ == '__main__':
    mnist = input_data.read_data_sets("./data/", one_hot=True)
    test(mnist)