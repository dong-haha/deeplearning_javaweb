import numpy as np
from .boxes_utils import assert_and_normalize_shape


def translate_boxes(boxes, x_shift=0, y_shift=0, copy=True):
    """translate boxes coordinates in x and y dimensions.
    
    Args:
        boxes: (N, 4+K)
        x_shift: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
            shift in x dimension
        y_shift: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
            shift in y dimension
        copy: bool
        
    References:
        `datasets.pipelines.RandomCrop` in mmdetection
    """
    boxes = np.array(boxes, dtype=np.float32, copy=copy)
    
    x_shift = np.asarray(x_shift, np.float32)
    y_shift = np.asarray(y_shift, np.float32)

    x_shift = assert_and_normalize_shape(x_shift, boxes.shape[0])
    y_shift = assert_and_normalize_shape(y_shift, boxes.shape[0])
    
    boxes[:, 0] += x_shift
    boxes[:, 1] += y_shift
    boxes[:, 2] += x_shift
    boxes[:, 3] += y_shift
    return boxes
    
    
def adjust_boxes(boxes, x_min_shift, y_min_shift, x_max_shift, y_max_shift, copy=True):
    """
    Args:
        boxes: (N, 4+K)
        x_min_shift: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
            shift (x_min, y_min) in x dimension
        y_min_shift: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
            shift (x_min, y_min) in y dimension
        x_max_shift: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
            shift (x_max, y_max) in x dimension
        y_max_shift: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
            shift (x_max, y_max) in y dimension
        copy: bool
    """
    boxes = np.array(boxes, dtype=np.float32, copy=copy)

    x_min_shift = np.asarray(x_min_shift, np.float32)
    y_min_shift = np.asarray(y_min_shift, np.float32)
    x_max_shift = np.asarray(x_max_shift, np.float32)
    y_max_shift = np.asarray(y_max_shift, np.float32)

    x_min_shift = assert_and_normalize_shape(x_min_shift, boxes.shape[0])
    y_min_shift = assert_and_normalize_shape(y_min_shift, boxes.shape[0])
    x_max_shift = assert_and_normalize_shape(x_max_shift, boxes.shape[0])
    y_max_shift = assert_and_normalize_shape(y_max_shift, boxes.shape[0])
    
    boxes[:, 0] += x_min_shift
    boxes[:, 1] += y_min_shift
    boxes[:, 2] += x_max_shift
    boxes[:, 3] += y_max_shift
    return boxes
    
    
def inflate_or_deflate_boxes(boxes, width_delta=0, height_delta=0, copy=True):
    """
    Args:
        boxes: (N, 4+K)
        width_delta: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
        height_delta: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
        copy: bool
    """
    boxes = np.array(boxes, dtype=np.float32, copy=copy)

    width_delta = np.asarray(width_delta, np.float32)
    height_delta = np.asarray(height_delta, np.float32)

    width_delta = assert_and_normalize_shape(width_delta, boxes.shape[0])
    height_delta = assert_and_normalize_shape(height_delta, boxes.shape[0])
    
    half_width_delta = width_delta * 0.5
    half_height_delta = height_delta * 0.5
    boxes[:, 0] -= half_width_delta
    boxes[:, 1] -= half_height_delta
    boxes[:, 2] += half_width_delta
    boxes[:, 3] += half_height_delta
    return boxes
    

def inflate_boxes_to_square(boxes, copy=True):
    """Inflate boxes to square
    Args:
        boxes: (N, 4+K)
        width_delta: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
        height_delta: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
        copy: bool
    """
    boxes = np.array(boxes, dtype=np.float32, copy=copy)

    widths = boxes[:, 2] - boxes[:, 0]
    heights = boxes[:, 3] - boxes[:, 1]
    max_side_lengths = np.maximum(widths, heights)
    
    width_deltas = np.subtract(max_side_lengths, widths, widths)
    height_deltas = np.subtract(max_side_lengths, heights, heights)
    width_deltas *= 0.5
    height_deltas *= 0.5
    boxes[:, 0] -= width_deltas
    boxes[:, 1] -= height_deltas
    boxes[:, 2] += width_deltas
    boxes[:, 3] += height_deltas
    return boxes
    

def deflate_boxes_to_square(boxes, copy=True):
    """Deflate boxes to square
    Args:
        boxes: (N, 4+K)
        width_delta: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
        height_delta: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
        copy: bool
    """
    boxes = np.array(boxes, dtype=np.float32, copy=copy)

    widths = boxes[:, 2] - boxes[:, 0]
    heights = boxes[:, 3] - boxes[:, 1]
    min_side_lengths = np.minimum(widths, heights)
    
    width_deltas = np.subtract(min_side_lengths, widths, widths)
    height_deltas = np.subtract(min_side_lengths, heights, heights)
    width_deltas *= 0.5
    height_deltas *= 0.5
    boxes[:, 0] -= width_deltas
    boxes[:, 1] -= height_deltas
    boxes[:, 2] += width_deltas
    boxes[:, 3] += height_deltas
    return boxes

