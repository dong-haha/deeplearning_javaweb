#!/bin/bash
source /root/miniconda3/bin/activate  /root/miniconda3/envs/tensorflow
cd /root/tomcat_python/mnist
python /root/tomcat_python/mnist/app_javaweb.py  $1 $2 
