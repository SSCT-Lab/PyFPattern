def compare_rules(r, rule):
    matched = False
    changed = False
    if (r['name'] == rule['name']):
        matched = True
        if (rule.get('description', None) != r['description']):
            changed = True
            r['description'] = rule['description']
        if (rule['protocol'] != r['protocol']):
            changed = True
            r['protocol'] = rule['protocol']
        if (str(rule['source_port_range']) != str(r['source_port_range'])):
            changed = True
            r['source_port_range'] = str(rule['source_port_range'])
        if (str(rule['destination_port_range']) != str(r['destination_port_range'])):
            changed = True
            r['destination_port_range'] = str(rule['destination_port_range'])
        if (rule['access'] != r['access']):
            changed = True
            r['access'] = rule['access']
        if (rule['priority'] != r['priority']):
            changed = True
            r['priority'] = rule['priority']
        if (rule['direction'] != r['direction']):
            changed = True
            r['direction'] = rule['direction']
    return (matched, changed)