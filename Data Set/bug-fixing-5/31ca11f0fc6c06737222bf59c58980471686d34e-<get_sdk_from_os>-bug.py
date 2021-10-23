def get_sdk_from_os(data):
    if (('name' not in data) or ('version' not in data)):
        return
    dsym_type = KNOWN_DSYM_TYPES.get(data['name'])
    if (dsym_type is None):
        return
    system_version = tuple((int(x) for x in (data['version'] + ('.0' * 3)).split('.')[:3]))
    return {
        'dsym_type': 'macho',
        'sdk_name': data['name'],
        'version_major': system_version[0],
        'version_minor': system_version[1],
        'version_patchlevel': system_version[2],
    }