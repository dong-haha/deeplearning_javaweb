import numpy as np


def assert_and_normalize_shape(x, length):
    """
    Args:
        x: ndarray
        length: int
    """
    if x.ndim == 0:
        return x
    elif x.ndim == 1:
        if len(x) == 1:
            return x
        elif len(x) == length:
            return x
        else:
            raise ValueError('Incompatible shape!')
    elif x.ndim == 2:
        if x.shape == (1, 1):
            return np.squeeze(x, axis=-1)
        elif x.shape == (length, 1):
            return np.squeeze(x, axis=-1)
        else:
            raise ValueError('Incompatible shape!') 
    else:
        raise ValueError('Incompatible ndim!')
        
        
def normalize_boxes(boxes, dtype=np.float32, copy=False, support_extra=True):
    boxes = np.array(boxes, dtype=dtype, copy=copy)
    assert boxes.ndim in [1, 2]
    last_dimension = boxes.shape[-1]
    if support_extra:
        assert last_dimension >= 4
    else:
        assert last_dimension == 4
        
    if boxes.ndim == 1:
        boxes = np.expand_dims(boxes, axis=0)
    return boxes
