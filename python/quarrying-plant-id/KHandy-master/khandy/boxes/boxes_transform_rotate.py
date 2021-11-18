import numpy as np
from .boxes_utils import assert_and_normalize_shape


def rotate_boxes(boxes, angle, x_center=0, y_center=0, scale=1, 
                 degrees=True, return_rotated_boxes=False):
    """
    Args:
        boxes: (N, 4+K)
        angle: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
        x_center: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
        y_center: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
        scale: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
            scale factor in x and y dimension
        degrees: bool
        return_rotated_boxes: bool
    """
    boxes = np.asarray(boxes, np.float32)
    
    angle = np.asarray(angle, np.float32)
    x_center = np.asarray(x_center, np.float32)
    y_center = np.asarray(y_center, np.float32)
    scale = np.asarray(scale, np.float32)
    
    angle = assert_and_normalize_shape(angle, boxes.shape[0])
    x_center = assert_and_normalize_shape(x_center, boxes.shape[0])
    y_center = assert_and_normalize_shape(y_center, boxes.shape[0])
    scale = assert_and_normalize_shape(scale, boxes.shape[0])
    
    if degrees:
        angle = np.deg2rad(angle)
    cos_val = scale * np.cos(angle)
    sin_val = scale * np.sin(angle)
    x_shift = x_center - x_center * cos_val + y_center * sin_val
    y_shift = y_center - x_center * sin_val - y_center * cos_val
    
    x_mins, y_mins = boxes[:,0], boxes[:,1]
    x_maxs, y_maxs = boxes[:,2], boxes[:,3]
    x00 = x_mins * cos_val - y_mins * sin_val + x_shift
    x10 = x_maxs * cos_val - y_mins * sin_val + x_shift
    x11 = x_maxs * cos_val - y_maxs * sin_val + x_shift
    x01 = x_mins * cos_val - y_maxs * sin_val + x_shift
    
    y00 = x_mins * sin_val + y_mins * cos_val + y_shift
    y10 = x_maxs * sin_val + y_mins * cos_val + y_shift
    y11 = x_maxs * sin_val + y_maxs * cos_val + y_shift
    y01 = x_mins * sin_val + y_maxs * cos_val + y_shift
    
    rotated_boxes = np.stack([x00, y00, x10, y10, x11, y11, x01, y01], axis=-1)
    ret_x_mins = np.min(rotated_boxes[:,0::2], axis=1)
    ret_y_mins = np.min(rotated_boxes[:,1::2], axis=1)
    ret_x_maxs = np.max(rotated_boxes[:,0::2], axis=1)
    ret_y_maxs = np.max(rotated_boxes[:,1::2], axis=1)
    
    if boxes.ndim == 4:
        ret_boxes = np.stack([ret_x_mins, ret_y_mins, ret_x_maxs, ret_y_maxs], axis=-1)
    else:
        ret_boxes = boxes.copy()
        ret_boxes[:, :4] = np.stack([ret_x_mins, ret_y_mins, ret_x_maxs, ret_y_maxs], axis=-1)
        
    if not return_rotated_boxes:
        return ret_boxes
    else:
        return ret_boxes, rotated_boxes
    
    
def rotate_boxes_wrt_centers(boxes, angle, scale=1, degrees=True,  
                             return_rotated_boxes=False):
    """
    Args:
        boxes: (N, 4+K)
        angle: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
        scale: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
            scale factor in x and y dimension
        degrees: bool
        return_rotated_boxes: bool
    """
    boxes = np.asarray(boxes, np.float32)
    
    angle = np.asarray(angle, np.float32)
    scale = np.asarray(scale, np.float32)
    angle = assert_and_normalize_shape(angle, boxes.shape[0])
    scale = assert_and_normalize_shape(scale, boxes.shape[0])
    
    if degrees:
        angle = np.deg2rad(angle)
    cos_val = scale * np.cos(angle)
    sin_val = scale * np.sin(angle)
    
    x_centers = boxes[:, 2] + boxes[:, 0]
    y_centers = boxes[:, 3] + boxes[:, 1]
    x_centers *= 0.5
    y_centers *= 0.5
    
    half_widths = boxes[:, 2] - boxes[:, 0]
    half_heights = boxes[:, 3] - boxes[:, 1]
    half_widths *= 0.5
    half_heights *= 0.5
    
    half_widths_cos = half_widths * cos_val
    half_widths_sin = half_widths * sin_val
    half_heights_cos = half_heights * cos_val
    half_heights_sin = half_heights * sin_val
    
    x00 = -half_widths_cos + half_heights_sin
    x10 = half_widths_cos + half_heights_sin
    x11 = half_widths_cos - half_heights_sin
    x01 = -half_widths_cos - half_heights_sin
    x00 += x_centers
    x10 += x_centers
    x11 += x_centers
    x01 += x_centers
    
    y00 = -half_widths_sin - half_heights_cos
    y10 = half_widths_sin - half_heights_cos
    y11 = half_widths_sin + half_heights_cos
    y01 = -half_widths_sin + half_heights_cos
    y00 += y_centers
    y10 += y_centers
    y11 += y_centers
    y01 += y_centers
    
    rotated_boxes = np.stack([x00, y00, x10, y10, x11, y11, x01, y01], axis=-1)
    ret_x_mins = np.min(rotated_boxes[:,0::2], axis=1)
    ret_y_mins = np.min(rotated_boxes[:,1::2], axis=1)
    ret_x_maxs = np.max(rotated_boxes[:,0::2], axis=1)
    ret_y_maxs = np.max(rotated_boxes[:,1::2], axis=1)
    
    if boxes.ndim == 4:
        ret_boxes = np.stack([ret_x_mins, ret_y_mins, ret_x_maxs, ret_y_maxs], axis=-1)
    else:
        ret_boxes = boxes.copy()
        ret_boxes[:, :4] = np.stack([ret_x_mins, ret_y_mins, ret_x_maxs, ret_y_maxs], axis=-1)
        
    if not return_rotated_boxes:
        return ret_boxes
    else:
        return ret_boxes, rotated_boxes
    
    