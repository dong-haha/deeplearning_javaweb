import numpy as np


def flip_image(image, direction='h', copy=True):
    """
    References:
        np.flipud, np.fliplr, np.flip
        cv2.flip
        tf.image.flip_up_down
        tf.image.flip_left_right
    """
    assert direction in ['x', 'h', 'horizontal',
                         'y', 'v', 'vertical', 
                         'o', 'b', 'both']
    if copy:
        image = image.copy()
    if direction in ['o', 'b', 'both', 'x', 'h', 'horizontal']:
        image = np.fliplr(image)
    if direction in ['o', 'b', 'both', 'y', 'v', 'vertical']:
        image = np.flipud(image)
    return image
    
    
def transpose_image(image, copy=True):
    """Transpose image.
    
    References:
        np.transpose
        cv2.transpose
        tf.image.transpose
    """
    if copy:
        image = image.copy()
    if image.ndim == 2:
        transpose_axes = (1, 0)
    else:
        transpose_axes = (1, 0, 2)
    image = np.transpose(image, transpose_axes)
    return image

    
def rot90_image(image, n=1, copy=True):
    """Rotate image counter-clockwise by 90 degrees.
    
    References:
        np.rot90
        tf.image.rot90
    """
    if copy:
        image = image.copy()
    if image.ndim == 2:
        transpose_axes = (1, 0)
    else:
        transpose_axes = (1, 0, 2)
        
    n = n % 4
    if n == 0:
        return image
    elif n == 1:
        image = np.transpose(image, transpose_axes)
        image = np.flipud(image)
    elif n == 2:
        image = np.fliplr(np.flipud(image))
    else:
        image = np.transpose(image, transpose_axes)
        image = np.fliplr(image)
    return image
