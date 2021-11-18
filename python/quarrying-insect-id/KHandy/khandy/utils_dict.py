import random
from collections import OrderedDict


def get_dict_first_item(dict_obj):
    for key in dict_obj:
        return key, dict_obj[key]


def sort_dict(dict_obj, key=None, reverse=False):
    return OrderedDict(sorted(dict_obj.items(), key=key, reverse=reverse))


def create_multidict(key_list, value_list):
    assert len(key_list) == len(value_list)
    multidict_obj = {}
    for key, value in zip(key_list, value_list):
        multidict_obj.setdefault(key, []).append(value)
    return multidict_obj


def convert_multidict_to_list(multidict_obj):
    key_list, value_list = [], []
    for key, value in multidict_obj.items():
        key_list += [key] * len(value)
        value_list += value
    return key_list, value_list


def convert_multidict_to_records(multidict_obj, key_map=None, raise_if_key_error=True):
    records = []
    if key_map is None:
        for key in multidict_obj:
            for value in multidict_obj[key]:
                records.append('{},{}'.format(value, key))
    else:
        for key in multidict_obj:
            if raise_if_key_error:
                mapped_key = key_map[key]
            else:
                mapped_key = key_map.get(key, key)
            for value in multidict_obj[key]:
                records.append('{},{}'.format(value, mapped_key))
    return records
    
    
def sample_multidict(multidict_obj, num_keys, num_per_key=None):
    num_keys = min(num_keys, len(multidict_obj))
    sub_keys = random.sample(list(multidict_obj), num_keys)
    if num_per_key is None:
        sub_mdict = {key: multidict_obj[key] for key in sub_keys}
    else:
        sub_mdict = {}
        for key in sub_keys:
            num_examples_inner = min(num_per_key, len(multidict_obj[key]))
            sub_mdict[key] = random.sample(multidict_obj[key], num_examples_inner)
    return sub_mdict
    
    
def split_multidict_on_key(multidict_obj, split_ratio, use_shuffle=False):
    """Split multidict_obj on its key.
    """
    assert isinstance(multidict_obj, dict)
    assert isinstance(split_ratio, (list, tuple))
    
    pdf = [k / float(sum(split_ratio)) for k in split_ratio]
    cdf = [sum(pdf[:k]) for k in range(len(pdf) + 1)]
    indices = [int(round(len(multidict_obj) * k)) for k in cdf]
    dict_keys = list(multidict_obj)
    if use_shuffle: 
        random.shuffle(dict_keys)
        
    be_split_list = []
    for i in range(len(split_ratio)):
        part_keys = dict_keys[indices[i]: indices[i + 1]]
        part_dict = dict([(key, multidict_obj[key]) for key in part_keys])
        be_split_list.append(part_dict)
    return be_split_list
    
    
def split_multidict_on_value(multidict_obj, split_ratio, use_shuffle=False):
    """Split multidict_obj on its value.
    """
    assert isinstance(multidict_obj, dict)
    assert isinstance(split_ratio, (list, tuple))
    
    pdf = [k / float(sum(split_ratio)) for k in split_ratio]
    cdf = [sum(pdf[:k]) for k in range(len(pdf) + 1)]
    be_split_list = [dict() for k in range(len(split_ratio))] 
    for key, value in multidict_obj.items():
        indices = [int(round(len(value) * k)) for k in cdf]
        cloned = value[:]
        if use_shuffle: 
            random.shuffle(cloned)
        for i in range(len(split_ratio)):
            be_split_list[i][key] = cloned[indices[i]: indices[i + 1]]
    return be_split_list
    
    
def get_multidict_info(multidict_obj, with_print=False, desc=None):
    num_list = [len(val) for val in multidict_obj.values()]
    num_keys = len(num_list)
    num_values = sum(num_list)
    max_values_per_key = max(num_list)
    min_values_per_key = min(num_list)
    if num_keys == 0:
        avg_values_per_key = 0
    else:
        avg_values_per_key = num_values / num_keys
    info = {
        'num_keys': num_keys,
        'num_values': num_values,
        'max_values_per_key': max_values_per_key,
        'min_values_per_key': min_values_per_key,
        'avg_values_per_key': avg_values_per_key,
    }
    if with_print:
        desc = desc or '<unknown>'
        print('{} key number:    {}'.format(desc, info['num_keys']))
        print('{} value number:    {}'.format(desc, info['num_values']))
        print('{} max number per-key: {}'.format(desc, info['max_values_per_key']))
        print('{} min number per-key: {}'.format(desc, info['min_values_per_key']))
        print('{} avg number per-key: {:.2f}'.format(desc, info['avg_values_per_key']))
    return info
    

def filter_multidict_by_number(multidict_obj, lower, upper=None):
    if upper is None:
        return {key: value for key, value in multidict_obj.items() 
                if lower <= len(value) }
    else:
        assert lower <= upper, 'lower must not be greater than upper'
        return {key: value for key, value in multidict_obj.items() 
                if lower <= len(value) <= upper }
        
        
def sort_multidict_by_number(multidict_obj, num_keys_to_keep=None, reverse=True):
    """
    Args:
        reverse: sort in ascending order when is True.
    """
    if num_keys_to_keep is None: 
        num_keys_to_keep = len(multidict_obj)
    else:
        num_keys_to_keep = min(num_keys_to_keep, len(multidict_obj))
    sorted_items = sorted(multidict_obj.items(), key=lambda x: len(x[1]), reverse=reverse)
    filtered_dict = OrderedDict()
    for i in range(num_keys_to_keep):
        filtered_dict[sorted_items[i][0]] = sorted_items[i][1]
    return filtered_dict

    
def merge_multidict(*mdicts):
    merged_multidict = {}
    for item in mdicts:
        for key, value in item.items():
            merged_multidict.setdefault(key, []).extend(value)
    return merged_multidict
    
    
def invert_multidict(multidict_obj):
    inverted_dict = {}
    for key, value in multidict_obj.items():
        for item in value:
            inverted_dict.setdefault(item, []).append(key)
    return inverted_dict
    
    