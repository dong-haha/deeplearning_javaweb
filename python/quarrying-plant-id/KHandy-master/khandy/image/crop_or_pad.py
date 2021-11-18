import numbers

import numpy as np


def crop_or_pad(image, x_min, y_min, x_max, y_max, border_value=0):
    """
    See Also:
        translate_image
        
    References:
        tf.image.resize_image_with_crop_or_pad
    """
    assert image.ndim in [2, 3]
    assert isinstance(x_min, numbers.Integral) and isinstance(y_min, numbers.Integral)
    assert isinstance(x_max, numbers.Integral) and isinstance(y_max, numbers.Integral)
    assert (x_min <= x_max) and (y_min <= y_max)
    
    src_height, src_width = image.shape[:2]
    dst_height, dst_width = y_max - y_min + 1, x_max - x_min + 1
    channels = 1 if image.ndim == 2 else image.shape[2]
    
    if image.ndim == 2: 
        dst_image_shape = (dst_height, dst_width)
    else:
        dst_image_shape = (dst_height, dst_width, channels)

    if isinstance(border_value, numbers.Real):
        dst_image = np.full(dst_image_shape, border_value, dtype=image.dtype)
    elif isinstance(border_value, tuple):
        assert len(border_value) == channels, \
            'Expected the num of elements in tuple equals the channels' \
            'of input image. Found {} vs {}'.format(
                len(border_value), channels)
        if channels == 1:
            dst_image = np.full(dst_image_shape, border_value[0], dtype=image.dtype)
        else:
            border_value = np.asarray(border_value, dtype=image.dtype)
            dst_image = np.empty(dst_image_shape, dtype=image.dtype)
            dst_image[:] = border_value
    else:
        raise ValueError(
            'Invalid type {} for `border_value`.'.format(type(border_value)))

    src_x_begin = max(x_min, 0)
    src_x_end   = min(x_max + 1, src_width)
    dst_x_begin = src_x_begin - x_min
    dst_x_end   = src_x_end - x_min

    src_y_begin = max(y_min, 0)
    src_y_end   = min(y_max + 1, src_height)
    dst_y_begin = src_y_begin - y_min
    dst_y_end   = src_y_end - y_min
    
    if (src_x_begin >= src_x_end) or (src_y_begin >= src_y_end):
        return dst_image
    dst_image[dst_y_begin: dst_y_end, dst_x_begin: dst_x_end, ...] = \
        image[src_y_begin: src_y_end, src_x_begin: src_x_end, ...]
    return dst_image
    
    
def center_crop(image, dst_width, dst_height):
    assert image.ndim in [2, 3]
    assert isinstance(dst_width, numbers.Integral) and isinstance(dst_height, numbers.Integral)
    assert (image.shape[0] >= dst_height) and (image.shape[1] >= dst_width)

    crop_top = (image.shape[0] - dst_height) // 2
    crop_left = (image.shape[1] - dst_width) // 2
    dst_image = image[crop_top: dst_height + crop_top, 
                      crop_left: dst_width + crop_left, ...]
    return dst_image
    
    
def crop_or_pad_coords(boxes, image_width, image_height):
    """
    References:
        `mmcv.impad`
        `pad` in https://github.com/kpzhang93/MTCNN_face_detection_alignment
        `MtcnnDetector.pad` in https://github.com/AITTSMD/MTCNN-Tensorflow
    """
    x_mins = boxes[:, 0]
    y_mins = boxes[:, 1]
    x_maxs = boxes[:, 2]
    y_maxs = boxes[:, 3]
    dst_widths = x_maxs - x_mins + 1
    dst_heights = y_maxs - y_mins + 1
    
    src_x_begin = np.maximum(x_mins, 0)
    src_x_end   = np.minimum(x_maxs + 1, image_width)
    dst_x_begin = src_x_begin - x_mins
    dst_x_end   = src_x_end - x_mins
    
    src_y_begin = np.maximum(y_mins, 0)
    src_y_end   = np.minimum(y_maxs + 1, image_height)
    dst_y_begin = src_y_begin - y_mins
    dst_y_end   = src_y_end - y_mins

    coords = np.stack([dst_y_begin, dst_y_end, dst_x_begin, dst_x_end, 
                       src_y_begin, src_y_end, src_x_begin, src_x_end, 
                       dst_heights, dst_widths], axis=0)
    return coords
    
    