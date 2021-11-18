import cv2
import numpy as np


def get_2d_rotation_matrix(angle, cx=0, cy=0, scale=1, 
                           degrees=True, dtype=np.float32):
    """
    References:
        `cv2.getRotationMatrix2D` in OpenCV
    """
    if degrees:
        angle = np.deg2rad(angle)
    c = scale * np.cos(angle)
    s = scale * np.sin(angle)

    tx = cx - cx * c + cy * s
    ty = cy - cx * s - cy * c
    return np.array([[ c, -s, tx],
                     [ s,  c, ty],
                     [ 0,  0, 1]], dtype=dtype)
    
    
def rotate_image(image, angle, scale=1.0, center=None, 
                 degrees=True, border_value=0, auto_bound=False):
    """Rotate an image.

    Args:
        image : ndarray
            Image to be rotated.
        angle : float
            Rotation angle in degrees, positive values mean clockwise rotation.
        center : tuple
            Center of the rotation in the source image, by default
            it is the center of the image.
        scale : float
            Isotropic scale factor.
        degrees : bool
        border_value : int
            Border value.
        auto_bound : bool
            Whether to adjust the image size to cover the whole rotated image.

    Returns:
        ndarray: The rotated image.
        
    References:
        mmcv.imrotate
    """
    image_height, image_width = image.shape[:2]
    if auto_bound:
        center = None
    if center is None:
        center = ((image_width - 1) * 0.5, (image_height - 1) * 0.5)
    assert isinstance(center, tuple)

    rotation_matrix = get_2d_rotation_matrix(angle, center[0], center[1], scale, degrees)
    if auto_bound:
        scale_cos = np.abs(rotation_matrix[0, 0])
        scale_sin = np.abs(rotation_matrix[0, 1])
        new_width = image_width * scale_cos + image_height * scale_sin
        new_height = image_width * scale_sin + image_height * scale_cos
        
        rotation_matrix[0, 2] += (new_width - image_width) * 0.5
        rotation_matrix[1, 2] += (new_height - image_height) * 0.5
        
        image_width = int(np.round(new_width))
        image_height = int(np.round(new_height))
    rotated = cv2.warpAffine(image, rotation_matrix[:2,:], (image_width, image_height), 
                             borderValue=border_value)
    return rotated
