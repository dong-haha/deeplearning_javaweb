import cv2
import numpy as np

from ..utils_numpy import minmax_normalize as _minmax_normalize


def normalize_image_dtype(image, keep_num_channels=False):
    """Normalize image dtype to uint8 (usually for visualization).
    
    Args:
        image : ndarray
            Input image.
        keep_num_channels : bool, optional
            If this is set to True, the result is an array which has 
            the same shape as input image, otherwise the result is 
            an array whose channels number is 3.
            
    Returns:
        out: ndarray
            Image whose dtype is np.uint8.
    """
    assert (image.ndim == 3 and image.shape[-1] in [1, 3]) or (image.ndim == 2)

    image = image.astype(np.float32)
    image = _minmax_normalize(image, axis=None, copy=False)
    image = np.array(image * 255, dtype=np.uint8)
    
    if not keep_num_channels:
        if image.ndim == 2:
            image = np.expand_dims(image, -1)
        if image.shape[-1] == 1:
            image = np.tile(image, (1,1,3))
    return image
    
    
def stack_image_list(image_list, dtype=np.float32):
    """Join a sequence of image along a new axis before first axis.

    References:
        `im_list_to_blob` in `py-faster-rcnn-master/lib/utils/blob.py`
    """
    assert isinstance(image_list, (tuple, list))

    max_dimension = np.array([image.ndim for image in image_list]).max()
    assert max_dimension in [2, 3]
    max_shape = np.array([image.shape[:2] for image in image_list]).max(axis=0)
    
    num_channels = []
    for image in image_list:
        if image.ndim == 2:
            num_channels.append(1)
        else:
            num_channels.append(image.shape[-1])
    assert len(set(num_channels) - set([1])) in [0, 1]
    max_num_channels = np.max(num_channels)
    
    blob = np.empty((len(image_list), max_shape[0], max_shape[1], max_num_channels), dtype=dtype)
    for k, image in enumerate(image_list):
        blob[k, :image.shape[0], :image.shape[1], :] = np.atleast_3d(image).astype(dtype, copy=False)
    if max_dimension == 2:
        blob = np.squeeze(blob, axis=-1)
    return blob
    
    
def is_gray_image(image, tol=3):
    if image.ndim == 2:
        return True
    elif image.ndim == 3:
        num_channels = image.shape[-1]
        if num_channels == 1:
            return True
        elif num_channels == 4:
            rgb = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
            gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
            gray3 = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            mae = np.mean(cv2.absdiff(rgb, gray3))
            return mae <= tol
        elif num_channels == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray3 = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            mae = np.mean(cv2.absdiff(image, gray3))
            return mae <= tol
        else:
            return False
    else:
        return False
        