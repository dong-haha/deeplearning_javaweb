import numpy as np


def clip_boxes(boxes, reference_box, copy=True):
    """Clip boxes to reference box.
    
    References:
        `clip_to_window` in TensorFlow object detection API.
    """
    x_min, y_min, x_max, y_max = reference_box[:4]
    boxes = np.array(boxes, dtype=np.float32, copy=copy)
    lower = np.array([[x_min, y_min, x_min, y_min]])
    upper = np.array([[x_max, y_max, x_max, y_max]])
    np.clip(boxes[:, :4], lower, upper, boxes[:,:4])
    return boxes
    
    
def clip_boxes_to_image(boxes, image_width, image_height, subpixel=True, copy=True):
    """Clip boxes to image boundaries.
    
    References:
        `clip_boxes` in py-faster-rcnn
        `core.boxes_op_list.clip_to_window` in TensorFlow object detection API.
        `structures.Boxes.clip` in detectron2
        
    Notes:
        Equivalent to `clip_boxes(boxes, [0,0,image_width-1,image_height-1], copy)`
    """
    boxes = np.array(boxes, dtype=np.float32, copy=copy)
    if not subpixel:
        image_width -= 1
        image_height -= 1
    np.clip(boxes[:, 0], 0, image_width,  boxes[:, 0])
    np.clip(boxes[:, 1], 0, image_height, boxes[:, 1])
    np.clip(boxes[:, 2], 0, image_width,  boxes[:, 2])
    np.clip(boxes[:, 3], 0, image_height, boxes[:, 3])
    return boxes
