import random


def to_list(obj):
    if obj is None:
        return None
    elif hasattr(obj, '__iter__') and not isinstance(obj, str):
        try:
            return list(obj)
        except:
            return [obj]
    else:
        return [obj]


def convert_lists_to_record(*list_objs, delimiter=None):
    assert len(list_objs) >= 1, 'list_objs length must >= 1.'
    delimiter = delimiter or ','

    assert isinstance(list_objs[0], (tuple, list))
    number = len(list_objs[0])
    for item in list_objs[1:]:
        assert isinstance(item, (tuple, list))
        assert len(item) == number, '{} != {}'.format(len(item), number)
        
    records = []
    record_list = zip(*list_objs)
    for record in record_list:
        record_str = [str(item) for item in record]
        records.append(delimiter.join(record_str))
    return records


def shuffle_table(*table):
    """
    Notes:
        table can be seen as list of list which have equal items.
    """
    shuffled_list = list(zip(*table))
    random.shuffle(shuffled_list)
    tuple_list = zip(*shuffled_list)
    return [list(item) for item in tuple_list]
    
    
def transpose_table(table):
    """
    Notes:
        table can be seen as list of list which have equal items.
    """
    m, n = len(table), len(table[0])
    return [[table[i][j] for i in range(m)] for j in range(n)]

