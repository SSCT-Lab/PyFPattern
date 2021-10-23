def to_dict(items, key, value):
    ' Transforms a list of items to a Key/Value dictionary '
    if items:
        return dict(zip([i.get(key) for i in items], [i.get(value) for i in items]))
    else:
        return dict()