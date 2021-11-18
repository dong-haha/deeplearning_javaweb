#!/bin/bash
source /root/miniconda3/bin/activate  /root/miniconda3/envs/tensorflow
python /root/tomcat_python/linear_regression.py  $1  $2  $3 $4
