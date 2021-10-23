def get_sdk_from_apple_system_info(info):
    if (not info):
        return None
    try:
        sdk_name = APPLE_SDK_MAPPING[info['system_name']]
        system_version = tuple((int(x) for x in (info['system_version'] + ('.0' * 3)).split('.')[:3]))
    except (ValueError, LookupError):
        return None
    return {
        'dsym_type': 'macho',
        'sdk_name': sdk_name,
        'version_major': system_version[0],
        'version_minor': system_version[1],
        'version_patchlevel': system_version[2],
    }