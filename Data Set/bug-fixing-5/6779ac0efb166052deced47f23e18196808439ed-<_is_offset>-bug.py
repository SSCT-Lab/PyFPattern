def _is_offset(self, arr_or_obj):
    ' check if obj or all elements of list-like is DateOffset '
    if isinstance(arr_or_obj, ABCDateOffset):
        return True
    elif (is_list_like(arr_or_obj) and len(arr_or_obj)):
        return all((isinstance(x, ABCDateOffset) for x in arr_or_obj))
    return False