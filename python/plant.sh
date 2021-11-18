#!/bin/bash
source /root/miniconda3/bin/activate  /root/miniconda3/envs/plantid
cd /root/tomcat_python/quarrying-plant-id
python /root/tomcat_python/quarrying-plant-id/predict.py  $1 $2  
