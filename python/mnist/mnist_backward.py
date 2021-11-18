import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import mnist_forward
import os

batch_size = 200
learning_rate_base = 0.1  # 初始学习率
learning_rate_decay = 0.99  # 学习率衰减率
regularizer = 0.0001  # 正则化系数
steps = 50000  # 训练轮数
moving_average_decay = 0.99
model_save_path = "./model/"  # 模型保存路径
model_name = "mnist_model"


def backward(mnist):
    x = tf.placeholder(tf.float32, [None, mnist_forward.INPUT_NODE])
    y_ = tf.placeholder(tf.float32, [None, mnist_forward.OUTPUT_NODE])
    y = mnist_forward.forward(x, regularizer)  # 调用forward()函数，设置正则化，计算y
    global_step = tf.Variable(0, trainable=False)  # 当前轮数计数器设定为不可训练类型

    # 调用包含所有参数正则化损失的损失函数loss
    ce = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=tf.argmax(y_, 1))
    cem = tf.reduce_mean(ce)
    loss = cem + tf.add_n(tf.get_collection('losses'))

    # 设定指数衰减学习率learning_rate
    learning_rate = tf.train.exponential_decay(
        learning_rate_base,
        global_step,
        mnist.train.num_examples / batch_size,
        learning_rate_decay,
        staircase=True
    )
    # 梯度衰减对模型优化，降低损失函数
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)

    # 定义参数的滑动平均
    ema = tf.train.ExponentialMovingAverage(moving_average_decay, global_step)
    ema_op = ema.apply(tf.trainable_variables())
    with tf.control_dependencies([train_step, ema_op]):
        train_op = tf.no_op(name='train')

    saver = tf.train.Saver()

    with tf.Session() as sess:
        init_op = tf.global_variables_initializer()  # 所有参数初始化
        sess.run(init_op)

        ckpt = tf.train.get_checkpoint_state(model_save_path)  # 加载指定路径下的滑动平均
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)

        for i in range(steps):  # 循环迭代steps轮
            xs, ys = mnist.train.next_batch(batch_size)
            _, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x: xs, y_: ys})
            if i % 1000 == 0:
                print("After %d training step(s),loss on training batch is %g." % (step, loss_value))
                saver.save(sess, os.path.join(model_save_path, model_name), global_step=global_step)  # 当前会话加载到指定路径


if __name__ == '__main__':
    mnist = input_data.read_data_sets("./data/", one_hot=True)
    backward(mnist)