def build_entry(etype, entity, permissions=None, use_nfsv4_acls=False):
    'Builds and returns an entry string. Does not include the permissions bit if they are not provided.'
    if use_nfsv4_acls:
        return ':'.join([etype, entity, permissions, 'allow'])
    if permissions:
        return ((((etype + ':') + entity) + ':') + permissions)
    return ((etype + ':') + entity)