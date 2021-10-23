

def ordered_merge(left, right, on=None, left_on=None, right_on=None, left_by=None, right_by=None, fill_method=None, suffixes=('_x', '_y')):
    warnings.warn('ordered_merge is deprecated and replaced by merge_ordered', FutureWarning, stacklevel=2)
    return merge_ordered(left, right, on=on, left_on=left_on, right_on=right_on, left_by=left_by, right_by=right_by, fill_method=fill_method, suffixes=suffixes)
