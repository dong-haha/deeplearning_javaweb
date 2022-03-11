## 概述
本项目为大三上学期的人工神经网络课程的结课论文而设计。  
主要将几个深度学习项目部署到网站 （植物、昆虫识别、yolo3目标检测、手写数字等） （plant  yolo3 insect deeplearning）   
前后端均未使用框架，代码简单，适合入门，重点放在python深度学习项目。
## 参考
植物识别：https://github.com/quarrying/quarrying-plant-id

昆虫识别：https://github.com/quarrying/quarrying-insect-id

yolo3 :https://github.com/bubbliiiing/yolo3-pytorch
## 详解
Javaweb：主要是前后端的代码。  
python： 每个具体项目的python代码。  
一共六个项目，除了线性回归只有一个py文件，其余的都对应相应文件夹。  
sh文件是为了java调用python而写。（这是一种java调用python的方法，但不是最好的，最好能把python写成单独的进程，通过进程通信交换数据）  
## 复现
除非和我的环境一模一样，否则几乎不能完全复现。
#### 1.有IDEA，linux服务器，懂python，Javaweb
先用idea导入javaweb文件夹，编译出war包，放到linux的tomcat下，重启。  
在linux下： 1. conda create 五个环境，每个对应一个项目。环境名看每个对应sh文件，需要哪些包自己想办法找  
           2.改路径，sh文件里面的路径改一下，或许python里的路径有些也要改,java也要改    
           3.补全文件。YOLO3，flower下有些文件太大，没上传，能在github上找到，毕竟我也是clone的   
#### 2.没有IDEA，不会web,会python
你可能无法使用Javaweb功能，但可以运行python项目。依旧conda出每个环境，然后进入对应文件夹，运行py文件。 
#### 3.没学过python
建议访问网站

## 网站
1.15.66.61/deeplearning
