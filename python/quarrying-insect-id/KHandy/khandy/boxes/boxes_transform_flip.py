import numpy as np
from .boxes_utils import assert_and_normalize_shape


def flip_boxes(boxes, x_center=0, y_center=0, direction='h'):
    """
    Args:
        boxes: (N, 4+K)
        x_center: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
        y_center: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
        direction: str
    """
    assert direction in ['x', 'h', 'horizontal',
                         'y', 'v', 'vertical', 
                         'o', 'b', 'both']
    boxes = np.asarray(boxes, np.float32)
    ret_boxes = boxes.copy()
    
    x_center = np.asarray(x_center, np.float32)
    y_center = np.asarray(y_center, np.float32)
    x_center = assert_and_normalize_shape(x_center, boxes.shape[0])
    y_center = assert_and_normalize_shape(y_center, boxes.shape[0])
    
    if direction in ['o', 'b', 'both', 'x', 'h', 'horizontal']:
        ret_boxes[:, 0] = 2 * x_center - boxes[:, 2] 
        ret_boxes[:, 2] = 2 * x_center - boxes[:, 0]
    if direction in ['o', 'b', 'both', 'y', 'v', 'vertical']:
        ret_boxes[:, 1] = 2 * y_center - boxes[:, 3]
        ret_boxes[:, 3] = 2 * y_center - boxes[:, 1]
    return ret_boxes
    
    
def fliplr_boxes(boxes, x_center=0, y_center=0):
    """
    Args:
        boxes: (N, 4+K)
        x_center: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
        y_center: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
    """
    boxes = np.asarray(boxes, np.float32)
    ret_boxes = boxes.copy()
    
    x_center = np.asarray(x_center, np.float32)
    y_center = np.asarray(y_center, np.float32)
    x_center = assert_and_normalize_shape(x_center, boxes.shape[0])
    y_center = assert_and_normalize_shape(y_center, boxes.shape[0])
     
    ret_boxes[:, 0] = 2 * x_center - boxes[:, 2] 
    ret_boxes[:, 2] = 2 * x_center - boxes[:, 0]
    return ret_boxes
    
    
def flipud_boxes(boxes, x_center=0, y_center=0):
    """
    Args:
        boxes: (N, 4+K)
        x_center: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
        y_center: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
    """
    boxes = np.asarray(boxes, np.float32)
    ret_boxes = boxes.copy()
    
    x_center = np.asarray(x_center, np.float32)
    y_center = np.asarray(y_center, np.float32)
    x_center = assert_and_normalize_shape(x_center, boxes.shape[0])
    y_center = assert_and_normalize_shape(y_center, boxes.shape[0])
    
    ret_boxes[:, 1] = 2 * y_center - boxes[:, 3]
    ret_boxes[:, 3] = 2 * y_center - boxes[:, 1]
    return ret_boxes
    
    
def transpose_boxes(boxes, x_center=0, y_center=0):
    """
    Args:
        boxes: (N, 4+K)
        x_center: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
        y_center: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
    """
    boxes = np.asarray(boxes, np.float32)
    ret_boxes = boxes.copy()
    
    x_center = np.asarray(x_center, np.float32)
    y_center = np.asarray(y_center, np.float32)
    x_center = assert_and_normalize_shape(x_center, boxes.shape[0])
    y_center = assert_and_normalize_shape(y_center, boxes.shape[0])
    
    shift = x_center - y_center
    ret_boxes[:, 0] = boxes[:, 1] + shift
    ret_boxes[:, 1] = boxes[:, 0] - shift
    ret_boxes[:, 2] = boxes[:, 3] + shift
    ret_boxes[:, 3] = boxes[:, 2] - shift
    return ret_boxes


def flip_boxes_in_image(boxes, image_width, image_height, direction='h'):
    """
    Args:
        boxes: (N, 4+K)
        image_width: int
        image_width: int
        direction: str
        
    References:
        `core.bbox.bbox_flip` in mmdetection
        `datasets.pipelines.RandomFlip.bbox_flip` in mmdetection
    """
    x_center = (image_width - 1) * 0.5
    y_center = (image_height - 1) * 0.5
    ret_boxes = flip_boxes(boxes, x_center, y_center, direction=direction)
    return ret_boxes
    
    
def rot90_boxes_in_image(boxes, image_width, image_height, n=1):
    """Rotate boxes counter-clockwise by 90 degrees.
    
    References:
        np.rot90
        tf.image.rot90
    """
    n = n % 4
    if n == 0:
        ret_boxes = boxes.copy()
    elif n == 1:
        ret_boxes = transpose_boxes(boxes)
        ret_boxes = flip_boxes_in_image(ret_boxes, image_width, image_height, 'v')
    elif n == 2:
        ret_boxes = flip_boxes_in_image(boxes, image_width, image_height, 'o')
    else:
        ret_boxes = transpose_boxes(boxes)
        ret_boxes = flip_boxes_in_image(ret_boxes, image_width, image_height, 'h');
    return ret_boxes
    
    