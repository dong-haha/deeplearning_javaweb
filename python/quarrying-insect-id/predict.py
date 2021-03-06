# -*- coding: UTF-8 -*-
import cv2
import khandy
import numpy as np
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import json
import sys

from insectid import InsectDetector
from insectid import InsectIdentifier


def imread_ex(filename, flags=-1):
    try:
        return cv2.imdecode(np.fromfile(filename, dtype=np.uint8), flags)
    except Exception as e:
        return None


def draw_text(image, text, position, font_size=20, color=(255, 0, 0),
              font_filename='data/simkai.ttf'):
    assert isinstance(color, (tuple, list)) and len(color) == 3
    gray = color[0]
    if isinstance(image, np.ndarray):
        pil_image = Image.fromarray(image)
        color = (color[2], color[1], color[0])
    elif isinstance(image, PIL.Image.Image):
        pil_image = image
    else:
        raise ValueError('Unsupported image type!')
    assert pil_image.mode in ['L', 'RGB', 'RGBA']
    if pil_image.mode == 'L':
        color = gray

    font_object = ImageFont.truetype(font_filename, size=font_size)
    drawable = ImageDraw.Draw(pil_image)
    drawable.text((position[0], position[1]), text,
                  fill=color, font=font_object)

    if isinstance(image, np.ndarray):
        return np.asarray(pil_image)
    return pil_image


if __name__ == '__main__':

    finally_result = []
    filename = sys.argv[1]
    image_name = sys.argv[2]

    finally_filename = filename.replace(image_name,'mark_'+image_name)

    #filename = './images/1.jpg'
    detector = InsectDetector()
    identifier = InsectIdentifier()

    image = imread_ex(filename)
    if max(image.shape[:2]) > 1280:
        image = khandy.resize_image_long(image, 1280)
    image_for_draw = image.copy()
    image_height, image_width = image.shape[:2]

    boxes, confs, classes = detector.detect(image)
    for box, conf, class_ind in zip(boxes, confs, classes):
        box_width = box[2] - box[0] + 1
        box_height = box[3] - box[1] + 1
        if box_width < 30 or box_height < 30:
            continue

        cropped = khandy.crop_or_pad(image, int(box[0]), int(box[1]), int(box[2]), int(box[3]))
        outputs = identifier.identify(cropped)
        if outputs['status'] == 0:
            outputs['image_name'] = 'mark_'+image_name
            finally_result.append(outputs)
            #print(type(outputs))
            prob = outputs['results'][0]['probability']
            if prob < 0.10:
                text = 'Unknown'
            else:
                text = '{}: {:.3f}'.format(outputs['results'][0]['chinese_name'],
                                           outputs['results'][0]['probability'])
            position = [int(box[0] + 2), int(box[1] - 20)]
            position[0] = min(max(position[0], 0), image_width)
            position[1] = min(max(position[1], 0), image_height)
            cv2.rectangle(image_for_draw, (int(box[0]), int(box[1])),
                          (int(box[2]), int(box[3])), (0, 255, 0), 2)

            image_for_draw = draw_text(image_for_draw, text, position)
    print(json.dumps(finally_result[0], ensure_ascii=False))

    cv2.imwrite(finally_filename, image_for_draw)
