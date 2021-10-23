def get_lun_mappings(ssid, api_url, user, pwd, get_all=None):
    mappings = ('storage-systems/%s/volume-mappings' % ssid)
    url = (api_url + mappings)
    (rc, data) = request(url, url_username=user, url_password=pwd)
    if (not get_all):
        remove_keys = ('ssid', 'perms', 'lunMappingRef', 'type', 'id')
        for key in remove_keys:
            for mapping in data:
                del mapping[key]
    return data