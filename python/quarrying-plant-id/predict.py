# -*- coding: UTF-8 -*-
import cv2
import plantid
import json
import sys

image_filename = sys.argv[1]
image_name = sys.argv[2]

plant_identifier = plantid.PlantIdentifier()
image = cv2.imread(image_filename)
outputs = plant_identifier.identify(image, topk=5)

outputs['image_name'] = image_name
if outputs['status'] == 0:
    print(json.dumps(outputs,ensure_ascii=False))
