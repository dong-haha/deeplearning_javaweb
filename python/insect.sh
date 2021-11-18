#!/bin/bash
source /root/miniconda3/bin/activate  /root/miniconda3/envs/insectid
cd /root/tomcat_python/quarrying-insect-id
python /root/tomcat_python/quarrying-insect-id/predict.py $1 $2  
