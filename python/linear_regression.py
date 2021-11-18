import numpy as np
import tensorflow as tf
import sys
import json

aa=sys.argv[1]
bb=sys.argv[2]
str_x=sys.argv[3].split(',')
str_y=sys.argv[4].split(',')

# 随机生成1000个点，围绕在y=0.1x+0.3的直线周围
#num_points = 1000
#vectors_set = []
#for i in range(num_points):
#    x1 = np.random.normal(0.0, 0.55)
#    y1 = x1 * 0.1 + 0.3 + np.random.normal(0.0, 0.03)
#    vectors_set.append([x1, y1])
#
## 生成一些样本
#x_data = [v[0] for v in vectors_set]
#y_data = [v[1] for v in vectors_set]

x_data=[float(i) for i in str_x]
y_data=[float(i) for i in str_y]

raw_data=[[x_data[i],y_data[i]] for i in range(0,len(x_data))]

learn_rate=float(aa)
max_time=int(bb)
# plt.scatter(x_data,y_data,c='r')
# plt.show()


# 生成1维的W矩阵，取值是[-1,1]之间的随机数
W = tf.Variable(tf.random_uniform([1], -1.0, 1.0), name='W')
# 生成1维的b矩阵，初始值是0
b = tf.Variable(tf.zeros([1]), name='b')
# 经过计算得出预估值y
y = W * x_data + b

# 以预估值y和实际值y_data之间的均方误差作为损失
loss = tf.reduce_mean(tf.square(y - y_data), name='loss')
# 采用梯度下降法来优化参数; 0.5为学习率
optimizer = tf.train.GradientDescentOptimizer(learn_rate)
# 训练的过程就是最小化这个误差值
train = optimizer.minimize(loss, name='train')

sess = tf.Session()

# 初始化变量
init = tf.global_variables_initializer()
sess.run(init)

# 初始化的W和b是多少


list1=[]
list2=[]
list1.append(np.array([sess.run(W)[0],sess.run(b)[0]]).tolist())
list2.append(np.array([sess.run(loss)]).tolist())

# 执行20次训练
for step in range(max_time):
    sess.run(train)
    # 输出训练好的W和b
    list1.append(np.array([sess.run(W)[0], sess.run(b)[0]]).tolist())
    list2.append(np.array([sess.run(loss)]).tolist())
dict1={}
dict2={}
dict1['data']=list1
dict1['loss']=list2
dict1['raw_data']=raw_data
if 'inf' in str(list1)+str(list2) or 'nan' in str(list1)+str(list2):
    dict2['true']=0
    dict2['error_data']=str(list1)+str(list2)
    print(json.dumps(dict2))
else:
    dict1['true']=1
    j = json.dumps(dict1)
    print(j)
