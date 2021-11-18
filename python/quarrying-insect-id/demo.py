import os
import time

import cv2
import khandy
import numpy as np
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from insectid import InsectDetector
from insectid import InsectIdentifier


def imread_ex(filename, flags=-1):
    try:
        return cv2.imdecode(np.fromfile(filename, dtype=np.uint8), flags)
    except Exception as e:
        return None
        
        
def draw_text(image, text, position, font_size=15, color=(255,0,0),
              font_filename='data/simsun.ttc'):
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
    src_dirs = [r'images', r'F:\_Data\Nature\_raw\_insect']
    
    detector = InsectDetector()
    identifier = InsectIdentifier()
    src_filenames = sum([khandy.get_all_filenames(src_dir) for src_dir in src_dirs], [])
    src_filenames = sorted(src_filenames, key=lambda t: os.stat(t).st_mtime, reverse=True)
    
    for k, filename in enumerate(src_filenames):
        print('[{}/{}] {}'.format(k+1, len(src_filenames), filename))
        start_time = time.time()
        image = imread_ex(filename)
        if image is None:
            continue
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
                print(outputs['results'][0])
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
                              (int(box[2]), int(box[3])), (0,255,0), 2)
                      
                image_for_draw = draw_text(image_for_draw, text, position)
        print('Elapsed: {:.3f}s'.format(time.time() - start_time))
        cv2.imshow('image', image_for_draw)
        key = cv2.waitKey(0)
        if key == 27:
            cv2.destroyAllWindows()
            break
            
