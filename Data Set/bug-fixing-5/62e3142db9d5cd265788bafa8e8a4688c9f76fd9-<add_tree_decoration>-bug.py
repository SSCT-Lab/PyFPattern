def add_tree_decoration(self, child_data, is_last_child, first_level):
    'Add tree curses decoration and indentation to a subtree.'
    pos = []
    for (i, m) in enumerate(child_data):
        if ((m['msg'] == '\n') and (m is not child_data[(- 1)])):
            pos.append((i + 12))
    new_child_data = []
    new_pos = []
    for (i, m) in enumerate(child_data):
        if (i in pos):
            new_pos.append(len(new_child_data))
            new_child_data.append(self.curse_add_line(''))
        new_child_data.append(m)
    child_data = new_child_data
    pos = new_pos
    if is_last_child:
        prefix = '└─'
    else:
        prefix = '├─'
    child_data[pos[0]]['msg'] = prefix
    for i in pos:
        spacing = 2
        if first_level:
            spacing = 1
        elif (is_last_child and (i is not pos[0])):
            spacing = 3
        child_data[i]['msg'] = ('%s%s' % ((' ' * spacing), child_data[i]['msg']))
    if (not is_last_child):
        for i in pos[1:]:
            old_str = child_data[i]['msg']
            if first_level:
                child_data[i]['msg'] = (' │' + old_str[2:])
            else:
                child_data[i]['msg'] = ((old_str[:2] + '│') + old_str[3:])
    return child_data