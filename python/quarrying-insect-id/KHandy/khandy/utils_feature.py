from collections import OrderedDict

import numpy as np

from .utils_dict import get_dict_first_item as _get_dict_first_item


def convert_feature_dict_to_array(feature_dict):
    one_feature = _get_dict_first_item(feature_dict)[1]
    num_features = sum([len(item) for item in feature_dict.values()])
    
    key_list = []
    start_index = 0
    feature_array = np.empty((num_features, one_feature.shape[-1]), one_feature.dtype)
    for key, value in feature_dict.items():
        feature_array[start_index: start_index + len(value)]= value
        key_list += [key] * len(value)
        start_index += len(value)
    return key_list, feature_array


def convert_feature_array_to_dict(key_list, feature_array):
    assert len(key_list) == len(feature_array)
    feature_dict = OrderedDict()
    for key, feat in zip(key_list, feature_array):
        feature_dict.setdefault(key, []).append(feat)
    for label in feature_dict.keys():
        feature_dict[label] = np.vstack(feature_dict[label])
    return feature_dict
    
    
def pairwise_distances(x, y, squared=True):
    """Compute pairwise (squared) Euclidean distances.
    
    References:
        [2016 CVPR] Deep Metric Learning via Lifted Structured Feature Embedding
        `euclidean_distances` from sklearn
    """
    assert isinstance(x, np.ndarray) and x.ndim == 2
    assert isinstance(y, np.ndarray) and y.ndim == 2
    assert x.shape[1] == y.shape[1]
    
    x_square = np.expand_dims(np.einsum('ij,ij->i', x, x), axis=1)
    if x is y:
        y_square = x_square.T
    else:
        y_square = np.expand_dims(np.einsum('ij,ij->i', y, y), axis=0)
    distances = np.dot(x, y.T)
    # use inplace operation to accelerate
    distances *= -2
    distances += x_square
    distances += y_square
    # result maybe less than 0 due to floating point rounding errors.
    np.maximum(distances, 0, distances)
    if x is y:
        # Ensure that distances between vectors and themselves are set to 0.0.
        # This may not be the case due to floating point rounding errors.
        distances.flat[::distances.shape[0] + 1] = 0.0
    if not squared:
        np.sqrt(distances, distances)
    return distances
    
    