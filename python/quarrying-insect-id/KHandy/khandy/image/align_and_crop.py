import cv2
import numpy as np


def get_similarity_transform(src_pts, dst_pts):
    """Get similarity transform matrix from src_pts to dst_pts
    
    Args:
        src_pts: Kx2 np.array
            source points matrix, each row is a pair of coordinates (x, y)
        dst_pts: Kx2 np.array
            destination points matrix, each row is a pair of coordinates (x, y)
            
    Returns:
        xform_matrix: 3x3 np.array
            transform matrix from src_pts to dst_pts
    """
    src_pts = np.asarray(src_pts)
    dst_pts = np.asarray(dst_pts)
    assert src_pts.shape == dst_pts.shape
    assert (src_pts.ndim == 2) and (src_pts.shape[-1] == 2)
    
    npts = src_pts.shape[0]
    src_x = src_pts[:, 0].reshape((-1, 1))
    src_y = src_pts[:, 1].reshape((-1, 1))
    tmp1 = np.hstack((src_x, -src_y, np.ones((npts, 1)), np.zeros((npts, 1))))
    tmp2 = np.hstack((src_y, src_x, np.zeros((npts, 1)), np.ones((npts, 1))))
    A = np.vstack((tmp1, tmp2))

    dst_x = dst_pts[:, 0].reshape((-1, 1))
    dst_y = dst_pts[:, 1].reshape((-1, 1))
    b = np.vstack((dst_x, dst_y))

    x = np.linalg.lstsq(A, b, rcond=-1)[0]
    x = np.squeeze(x)
    sc, ss, tx, ty = x[0], x[1], x[2], x[3]
    xform_matrix = np.array([
        [sc, -ss, tx],
        [ss,  sc, ty],
        [ 0,   0,  1]
    ])
    return xform_matrix
    
    
def align_and_crop(image, landmarks, std_landmarks, align_size, 
                   border_value=0, return_transform_matrix=False):
    landmarks = np.asarray(landmarks)
    std_landmarks = np.asarray(std_landmarks)
    xform_matrix = get_similarity_transform(landmarks, std_landmarks)

    landmarks_ex = np.pad(landmarks, ((0,0),(0,1)), mode='constant', constant_values=1)
    dst_landmarks = np.dot(landmarks_ex, xform_matrix[:2,:].T)
    dst_image = cv2.warpAffine(image, xform_matrix[:2,:], dsize=align_size, 
                               borderValue=border_value)
    if return_transform_matrix:
        return dst_image, dst_landmarks, xform_matrix
    else:
        return dst_image, dst_landmarks
        
        