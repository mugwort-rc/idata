def make_slice_list(indexes):
    """
    >>> make_slice_list([])
    []
    >>> make_slice_list([0])
    [slice(0, 1, None)]
    >>> make_slice_list([0, 1, 2])
    [slice(0, 3, None)]
    >>> make_slice_list([0, 2, 3, 10])
    [slice(0, 1, None), slice(2, 4, None), slice(10, 11, None)]
    """
    if len(indexes) == 0:
        return []
    tmp = []
    start = indexes[0]
    last = start
    current = last
    for current in indexes[1:]:
        assert current > last
        if current - last != 1:
            tmp.append(slice(start, last+1))
            start = current
            last = start
        else:
            last = current
    if current == last:
        tmp.append(slice(start, last+1))
    return tmp
