def diff_list_of_dicts(w, h):
    '\n    Returns a list containing diff between\n    two list of dictionaries\n    '
    if (not w):
        w = []
    if (not h):
        h = []
    diff = []
    set_w = set((tuple(d.items()) for d in w))
    set_h = set((tuple(d.items()) for d in h))
    difference = set_w.difference(set_h)
    for element in difference:
        diff.append(dict(((x, y) for (x, y) in element)))
    return diff