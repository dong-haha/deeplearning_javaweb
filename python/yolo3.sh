#!/bin/bash
source /root/miniconda3/bin/activate  /root/miniconda3/envs/mypytorch
cd /root/tomcat_python/yolo3-pytorch
python /root/tomcat_python/yolo3-pytorch/predict.py  $1 $2 
