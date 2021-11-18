import numpy as np


def filter_small_boxes(boxes, min_width, min_height):
    """Filters all boxes with side smaller than min size. 

    Args:
        boxes: a numpy array with shape [N, 4] holding N boxes.
        min_width (float): minimum width
        min_height (float): minimum height

    Returns:
        keep: indices of the boxes that have width larger than
            min_width and height larger than min_height.

    References:
        `_filter_boxes` in py-faster-rcnn
        `prune_small_boxes` in TensorFlow object detection API.
        `structures.Boxes.nonempty` in detectron2
        `ops.boxes.remove_small_boxes` in torchvision
    """
    widths = boxes[:, 2] - boxes[:, 0]
    heights = boxes[:, 3] - boxes[:, 1] 
    keep = (widths >= min_width)
    keep &= (heights >= min_height)
    return np.nonzero(keep)[0]
    

def filter_boxes_outside(boxes, reference_box):
    """Filters bounding boxes that fall outside reference box.
    
    References:
        `prune_outside_window` in TensorFlow object detection API.
    """
    x_min, y_min, x_max, y_max = reference_box[:4]
    keep = ((boxes[:, 0] >= x_min) & (boxes[:, 1] >= y_min) &
            (boxes[:, 2] <= x_max) & (boxes[:, 3] <= y_max))
    return np.nonzero(keep)[0]


def filter_boxes_completely_outside(boxes, reference_box):
    """Filters bounding boxes that fall completely outside of reference box.
    
    References:
        `prune_completely_outside_window` in TensorFlow object detection API.
    """
    x_min, y_min, x_max, y_max = reference_box[:4]
    keep = ((boxes[:, 0] < x_max) & (boxes[:, 1] < y_max) &
            (boxes[:, 2] > x_min) & (boxes[:, 3] > y_min))
    return np.nonzero(keep)[0]
    

def non_max_suppression(boxes, scores, thresh, classes=None, ratio_type="iou"):
    """Greedily select boxes with high confidence
    Args:
        boxes: [[x_min, y_min, x_max, y_max], ...]
        scores: object confidence
        thresh: retain overlap_ratio <= thresh
        classes: class labels
        
    Returns:
        indexes to keep
        
    References:
        `py_cpu_nms` in py-faster-rcnn
        torchvision.ops.nms
        torchvision.ops.batched_nms
    """

    if boxes.size == 0:
        return np.empty((0,), dtype=np.int64)
    if classes is not None:
        # strategy: in order to perform NMS independently per class,
        # we add an offset to all the boxes. The offset is dependent
        # only on the class idx, and is large enough so that boxes
        # from different classes do not overlap
        max_coordinate = np.max(boxes)
        offsets = classes * (max_coordinate + 1)
        boxes = boxes + offsets[:, None]
    
    x_mins = boxes[:, 0]
    y_mins = boxes[:, 1]
    x_maxs = boxes[:, 2]
    y_maxs = boxes[:, 3]
    areas = (x_maxs - x_mins) * (y_maxs - y_mins)
    order = scores.flatten().argsort()[::-1]
    
    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        
        max_x_mins = np.maximum(x_mins[i], x_mins[order[1:]])
        max_y_mins = np.maximum(y_mins[i], y_mins[order[1:]])
        min_x_maxs = np.minimum(x_maxs[i], x_maxs[order[1:]])
        min_y_maxs = np.minimum(y_maxs[i], y_maxs[order[1:]])
        widths = np.maximum(0, min_x_maxs - max_x_mins)
        heights = np.maximum(0, min_y_maxs - max_y_mins)
        intersect_area = widths * heights
        
        if ratio_type in ["union", 'iou']:
            ratio = intersect_area / (areas[i] + areas[order[1:]] - intersect_area)
        elif ratio_type == "min":
            ratio = intersect_area / np.minimum(areas[i], areas[order[1:]])
        else:
            raise ValueError('Unsupported ratio_type. Got {}'.format(ratio_type))
            
        inds = np.nonzero(ratio <= thresh)[0]
        order = order[inds + 1]
    return np.asarray(keep)
    