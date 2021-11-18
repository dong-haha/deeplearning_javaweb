import numpy as np


def _concat(arr_list, axis=0):
    """Avoids a copy if there is only a single element in a list.
    """
    if len(arr_list) == 1:
        return arr_list[0]
    return np.concatenate(arr_list, axis)
    
    
def convert_boxes_list_to_boxes_and_indices(boxes_list):
    """
    Args:
        boxes_list (np.ndarray): list or tuple of ndarray with shape (N_i, 4+K)
        
    Returns:
        boxes (ndarray): shape (M, 4+K) where M is sum of N_i.
        indices (ndarray): shape (M, 1) where M is sum of N_i.
        
    References:
        `mmdet.core.bbox.bbox2roi` in mmdetection
        `convert_boxes_to_roi_format` in TorchVision
        `modeling.poolers.convert_boxes_to_pooler_format` in detectron2
    """
    assert isinstance(boxes_list, (list, tuple))
    boxes = _concat(boxes_list, axis=0)
    
    indices_list = [np.full((len(b), 1), i, boxes.dtype) 
                    for i, b in enumerate(boxes_list)]
    indices = _concat(indices_list, axis=0)
    return boxes, indices
    
    
def convert_boxes_and_indices_to_boxes_list(boxes, indices, num_indices):
    """
    Args:
        boxes (np.ndarray): shape (N, 4+K)
        indices (np.ndarray): shape (N,) or (N, 1), maybe batch index 
            in mini-batch or class label index.
        num_indices (int): number of index.

    Returns:
        list (ndarray): boxes list of each index
        
    References:
        `mmdet.core.bbox2result` in mmdetection
        `mmdet.core.bbox.roi2bbox` in mmdetection
        `convert_boxes_to_roi_format` in TorchVision
        `modeling.poolers.convert_boxes_to_pooler_format` in detectron2
    """
    boxes = np.asarray(boxes)
    indices = np.asarray(indices)
    assert boxes.ndim == 2, "boxes ndim must be 2, got {}".format(boxes.ndim)
    assert (indices.ndim == 1) or (indices.ndim == 2 and indices.shape[-1] == 1), \
        "indices ndim must be 1 or 2 if last dimension size is 1, got shape {}".format(indices.shape)
    assert boxes.shape[0] == indices.shape[0], "the 1st dimension size of boxes and indices "\
        "must be the same, got {} != {}".format(boxes.shape[0], indices.shape[0])
        
    if boxes.shape[0] == 0:
        return [np.zeros((0, boxes.shape[1]), dtype=np.float32) 
                for i in range(num_indices)]
    else:
        if indices.ndim == 2:
            indices = np.squeeze(indices, axis=-1)
        return [boxes[indices == i, :] for i in range(num_indices)]
    
    