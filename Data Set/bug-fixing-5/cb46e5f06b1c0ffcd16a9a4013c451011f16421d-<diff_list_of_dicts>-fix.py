def diff_list_of_dicts(self, want, have):
    if (not want):
        want = []
    if (not have):
        have = []
    diff = []
    for w_item in want:
        h_item = (search_obj_in_list(w_item['member'], have, key='member') or {
            
        })
        delta = dict_diff(h_item, w_item)
        if delta:
            if ('member' not in delta.keys()):
                delta['member'] = w_item['member']
            diff.append(delta)
    return diff