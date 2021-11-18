import numpy as np


def paired_intersection(boxes1, boxes2):
    """Compute paired intersection areas between boxes.
    Args:
        boxes1: a numpy array with shape [N, 4] holding N boxes
        boxes2: a numpy array with shape [N, 4] holding N boxes
        
    Returns:
        a numpy array with shape [N,] representing itemwise intersection area
        
    References:
        `core.box_list_ops.matched_intersection` in Tensorflow object detection API
        
    Notes:
        can called as itemwise_intersection, matched_intersection, aligned_intersection
    """
    max_x_mins = np.maximum(boxes1[:, 0], boxes2[:, 0])
    max_y_mins = np.maximum(boxes1[:, 1], boxes2[:, 1])
    min_x_maxs = np.minimum(boxes1[:, 2], boxes2[:, 2])
    min_y_maxs = np.minimum(boxes1[:, 3], boxes2[:, 3])
    intersect_widths = np.maximum(0, min_x_maxs - max_x_mins)
    intersect_heights = np.maximum(0, min_y_maxs - max_y_mins)
    return intersect_widths * intersect_heights
    
    
def pairwise_intersection(boxes1, boxes2):
    """Compute pairwise intersection areas between boxes.
    
    Args:
        boxes1: a numpy array with shape [N, 4] holding N boxes.
        boxes2: a numpy array with shape [M, 4] holding M boxes.
        
    Returns:
        a numpy array with shape [N, M] representing pairwise intersection area.
        
    References:
        `core.box_list_ops.intersection` in Tensorflow object detection API
        `utils.box_list_ops.intersection` in Tensorflow object detection API
    """
    if boxes1.shape[0] * boxes2.shape[0] == 0:
        return np.zeros((boxes1.shape[0], boxes2.shape[0]), dtype=boxes1.dtype)

    swap = False
    if boxes1.shape[0] > boxes2.shape[0]:
        boxes1, boxes2 = boxes2, boxes1
        swap = True
    intersect_areas = np.empty((boxes1.shape[0], boxes2.shape[0]), dtype=boxes1.dtype)

    for i in range(boxes1.shape[0]):
        max_x_mins = np.maximum(boxes1[i, 0], boxes2[:, 0])
        max_y_mins = np.maximum(boxes1[i, 1], boxes2[:, 1])
        min_x_maxs = np.minimum(boxes1[i, 2], boxes2[:, 2])
        min_y_maxs = np.minimum(boxes1[i, 3], boxes2[:, 3])
        intersect_widths = np.maximum(0, min_x_maxs - max_x_mins)
        intersect_heights = np.maximum(0, min_y_maxs - max_y_mins)
        intersect_areas[i, :] = intersect_widths * intersect_heights
    if swap:
        intersect_areas = intersect_areas.T
    return intersect_areas
    
    
def paired_overlap_ratio(boxes1, boxes2, ratio_type='iou'):
    """Compute paired overlap ratio between boxes.
    
    Args:
        boxes1: a numpy array with shape [N, 4] holding N boxes
        boxes2: a numpy array with shape [N, 4] holding N boxes
        ratio_type:
            iou: Intersection-over-union (iou).
            ioa: Intersection-over-area (ioa) between two boxes box1 and box2 is defined as
                their intersection area over box2's area. Note that ioa is not symmetric,
                that is, IOA(box1, box2) != IOA(box2, box1).
            min: Compute the ratio as the area of intersection between box1 and box2, 
                divided by the minimum area of the two bounding boxes.
                
    Returns:
        a numpy array with shape [N,] representing itemwise overlap ratio.
        
    References:
        `core.box_list_ops.matched_iou` in Tensorflow object detection API
        `structures.boxes.matched_boxlist_iou` in detectron2
        `mmdet.core.bbox.bbox_overlaps`, see https://mmdetection.readthedocs.io/en/v2.17.0/api.html#mmdet.core.bbox.bbox_overlaps
    """
    intersect_areas = paired_intersection(boxes1, boxes2)
    areas1 = (boxes1[:, 2] - boxes1[:, 0]) * (boxes1[:, 3] - boxes1[:, 1])
    areas2 = (boxes2[:, 2] - boxes2[:, 0]) * (boxes2[:, 3] - boxes2[:, 1])
    
    if ratio_type in ['union', 'iou', 'giou']:
        union_areas = areas1 - intersect_areas
        union_areas += areas2
        intersect_areas /= union_areas
    elif ratio_type == 'min':
        min_areas = np.minimum(areas1, areas2)
        intersect_areas /= min_areas
    elif ratio_type == 'ioa':
        intersect_areas /= areas2
    else:
        raise ValueError('Unsupported ratio_type. Got {}'.format(ratio_type))
        
    if ratio_type == 'giou':
        min_xy_mins = np.minimum(boxes1[:, 0:2], boxes2[:, 0:2])
        max_xy_mins = np.maximum(boxes1[:, 2:4], boxes2[:, 2:4])
        # mebb = minimum enclosing bounding boxes
        mebb_whs = np.maximum(0, max_xy_mins - min_xy_mins)
        mebb_areas = mebb_whs[:, 0] * mebb_whs[:, 1]
        union_areas -= mebb_areas
        union_areas /= mebb_areas
        intersect_areas += union_areas
    return intersect_areas


def pairwise_overlap_ratio(boxes1, boxes2, ratio_type='iou'):
    """Compute pairwise overlap ratio between boxes.
    
    Args:
        boxes1: a numpy array with shape [N, 4] holding N boxes
        boxes2: a numpy array with shape [M, 4] holding M boxes
        ratio_type:
            iou: Intersection-over-union (iou).
            ioa: Intersection-over-area (ioa) between two boxes box1 and box2 is defined as
                their intersection area over box2's area. Note that ioa is not symmetric,
                that is, IOA(box1, box2) != IOA(box2, box1).
            min: Compute the ratio as the area of intersection between box1 and box2, 
                divided by the minimum area of the two bounding boxes.
    Returns:
        a numpy array with shape [N, M] representing pairwise overlap ratio.
        
    References:
        `utils.np_box_ops.iou` in Tensorflow object detection API
        `utils.np_box_ops.ioa` in Tensorflow object detection API
        `utils.np_box_ops.giou` in Tensorflow object detection API
        `mmdet.core.bbox.bbox_overlaps`, see https://mmdetection.readthedocs.io/en/v2.17.0/api.html#mmdet.core.bbox.bbox_overlaps
        `torchvision.ops.box_iou`, see https://pytorch.org/vision/stable/ops.html#torchvision.ops.box_iou
        `torchvision.ops.generalized_box_iou`, see https://pytorch.org/vision/stable/ops.html#torchvision.ops.generalized_box_iou
        http://ww2.mathworks.cn/help/vision/ref/bboxoverlapratio.html
    """
    intersect_areas = pairwise_intersection(boxes1, boxes2)
    areas1 = (boxes1[:, 2] - boxes1[:, 0]) * (boxes1[:, 3] - boxes1[:, 1])
    areas2 = (boxes2[:, 2] - boxes2[:, 0]) * (boxes2[:, 3] - boxes2[:, 1])
    
    if ratio_type in ['union', 'iou', 'giou']:
        union_areas = np.expand_dims(areas1, axis=1) - intersect_areas
        union_areas += np.expand_dims(areas2, axis=0)
        intersect_areas /= union_areas
    elif ratio_type == 'min':
        min_areas = np.minimum(np.expand_dims(areas1, axis=1), np.expand_dims(areas2, axis=0))
        intersect_areas /= min_areas
    elif ratio_type == 'ioa':
        intersect_areas /= np.expand_dims(areas2, axis=0)
    else:
        raise ValueError('Unsupported ratio_type. Got {}'.format(ratio_type))
        
    if ratio_type == 'giou':
        min_xy_mins = np.minimum(boxes1[:, None, 0:2], boxes2[:, 0:2])
        max_xy_mins = np.maximum(boxes1[:, None, 2:4], boxes2[:, 2:4])
        # mebb = minimum enclosing bounding boxes
        mebb_whs = np.maximum(0, max_xy_mins - min_xy_mins)
        mebb_areas = mebb_whs[:, :, 0] * mebb_whs[:, :, 1]
        union_areas -= mebb_areas
        union_areas /= mebb_areas
        intersect_areas += union_areas
    return intersect_areas
    
