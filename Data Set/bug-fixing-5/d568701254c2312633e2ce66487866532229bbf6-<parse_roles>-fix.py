def parse_roles(data):
    configured_roles = None
    if ('TABLE_role' in data):
        configured_roles = data.get('TABLE_role')['ROW_role']
    roles = list()
    if configured_roles:
        for item in to_list(configured_roles):
            roles.append(item['role'])
    return roles