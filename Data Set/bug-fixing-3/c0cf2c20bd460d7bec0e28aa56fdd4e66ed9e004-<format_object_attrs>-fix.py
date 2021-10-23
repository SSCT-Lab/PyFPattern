def format_object_attrs(obj: Sequence, include_dtype: bool=True) -> List[Tuple[(str, Union[(str, int)])]]:
    "\n    Return a list of tuples of the (attr, formatted_value)\n    for common attrs, including dtype, name, length\n\n    Parameters\n    ----------\n    obj : object\n        must be iterable\n    include_dtype : bool\n        If False, dtype won't be in the returned list\n\n    Returns\n    -------\n    list of 2-tuple\n\n    "
    attrs: List[Tuple[(str, Union[(str, int)])]] = []
    if (hasattr(obj, 'dtype') and include_dtype):
        attrs.append(('dtype', f"'{obj.dtype}'"))
    if (getattr(obj, 'name', None) is not None):
        attrs.append(('name', default_pprint(obj.name)))
    elif ((getattr(obj, 'names', None) is not None) and any(obj.names)):
        attrs.append(('names', default_pprint(obj.names)))
    max_seq_items = (get_option('display.max_seq_items') or len(obj))
    if (len(obj) > max_seq_items):
        attrs.append(('length', len(obj)))
    return attrs