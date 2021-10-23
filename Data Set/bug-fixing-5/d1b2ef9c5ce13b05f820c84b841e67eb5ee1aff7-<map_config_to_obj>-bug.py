def map_config_to_obj(module):
    data = get_config(module, flags=['| section username'])
    match = re.findall('(?:^(?:u|\\s{2}u))sername (\\S+)', data, re.M)
    if (not match):
        return list()
    instances = list()
    for user in set(match):
        regex = ('username %s .+$' % user)
        cfg = re.findall(regex, data, re.M)
        cfg = '\n'.join(cfg)
        obj = {
            'name': user,
            'state': 'present',
            'nopassword': ('nopassword' in cfg),
            'configured_password': None,
            'hashed_password': None,
            'password_type': parse_password_type(cfg),
            'sshkey': parse_sshkey(data, user),
            'privilege': parse_privilege(cfg),
            'view': parse_view(cfg),
        }
        instances.append(obj)
    return instances