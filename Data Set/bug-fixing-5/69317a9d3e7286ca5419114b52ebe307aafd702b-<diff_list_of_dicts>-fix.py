def diff_list_of_dicts(w, h):
    '\n    Returns a list containing diff between\n    two list of dictionaries\n    '
    if (not w):
        w = []
    if (not h):
        h = []
    diff = []
    for w_item in w:
        h_item = (search_obj_in_list(w_item['member'], h, key='member') or {
            
        })
        d = dict_diff(h_item, w_item)
        if d:
            if ('member' not in d.keys()):
                d['member'] = w_item['member']
            diff.append(d)
    return diff