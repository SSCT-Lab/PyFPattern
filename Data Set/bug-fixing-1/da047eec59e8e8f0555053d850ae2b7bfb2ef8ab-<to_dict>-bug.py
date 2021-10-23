

def to_dict(items, key, value):
    ' Transforms a list of items to a Key/Value dictionary '
    if items:
        return dict(zip([i[key] for i in items], [i[value] for i in items]))
    else:
        return dict()
