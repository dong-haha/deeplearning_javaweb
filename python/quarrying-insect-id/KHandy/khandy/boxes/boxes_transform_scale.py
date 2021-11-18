import numpy as np
from .boxes_utils import assert_and_normalize_shape


def scale_boxes(boxes, x_scale=1, y_scale=1, x_center=0, y_center=0, copy=True):
    """Scale boxes coordinates in x and y dimensions.
    
    Args:
        boxes: (N, 4+K)
        x_scale: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
            scale factor in x dimension
        y_scale: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
            scale factor in y dimension
        x_center: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
        y_center: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
        
    References:
        `core.box_list_ops.scale` in TensorFlow object detection API
        `utils.box_list_ops.scale` in TensorFlow object detection API
        `datasets.pipelines.Resize._resize_bboxes` in mmdetection
        `core.anchor.guided_anchor_target.calc_region` in mmdetection where comments may be misleading!
        `layers.mask_ops.scale_boxes` in detectron2
        `mmcv.bbox_scaling`
    """
    boxes = np.array(boxes, dtype=np.float32, copy=copy)

    x_scale = np.asarray(x_scale, np.float32)
    y_scale = np.asarray(y_scale, np.float32)
    x_scale = assert_and_normalize_shape(x_scale, boxes.shape[0])
    y_scale = assert_and_normalize_shape(y_scale, boxes.shape[0])
    
    x_center = np.asarray(x_center, np.float32)
    y_center = np.asarray(y_center, np.float32)
    x_center = assert_and_normalize_shape(x_center, boxes.shape[0])
    y_center = assert_and_normalize_shape(y_center, boxes.shape[0])
    
    x_shift = 1 - x_scale
    y_shift = 1 - y_scale
    x_shift *= x_center
    y_shift *= y_center
    
    boxes[:, 0] *= x_scale
    boxes[:, 1] *= y_scale
    boxes[:, 2] *= x_scale
    boxes[:, 3] *= y_scale
    boxes[:, 0] += x_shift
    boxes[:, 1] += y_shift
    boxes[:, 2] += x_shift
    boxes[:, 3] += y_shift
    return boxes
    
    
def scale_boxes_wrt_centers(boxes, x_scale=1, y_scale=1, copy=True):
    """
    Args:
        boxes: (N, 4+K)
        x_scale: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
            scale factor in x dimension
        y_scale: array-like whose shape is (), (1,), (N,), (1, 1) or (N, 1)
            scale factor in y dimension
            
    References:
        `core.anchor.guided_anchor_target.calc_region` in mmdetection where comments may be misleading!
        `layers.mask_ops.scale_boxes` in detectron2
        `mmcv.bbox_scaling`
    """
    boxes = np.array(boxes, dtype=np.float32, copy=copy)
    
    x_scale = np.asarray(x_scale, np.float32)
    y_scale = np.asarray(y_scale, np.float32)
    x_scale = assert_and_normalize_shape(x_scale, boxes.shape[0])
    y_scale = assert_and_normalize_shape(y_scale, boxes.shape[0])
    
    x_factor = (x_scale - 1) * 0.5
    y_factor = (y_scale - 1) * 0.5
    x_deltas = boxes[:, 2] - boxes[:, 0]
    y_deltas = boxes[:, 3] - boxes[:, 1]
    x_deltas *= x_factor
    y_deltas *= y_factor

    boxes[:, 0] -= x_deltas
    boxes[:, 1] -= y_deltas
    boxes[:, 2] += x_deltas
    boxes[:, 3] += y_deltas
    return boxes

