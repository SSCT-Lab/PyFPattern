def create_mapping(module, ssid, lun_map, vol_name, api_url, user, pwd, validate_certs):
    mappings = ('storage-systems/%s/volume-mappings' % ssid)
    url = (api_url + mappings)
    if (lun_map is not None):
        post_body = json.dumps(dict(mappableObjectId=lun_map['volumeRef'], targetId=lun_map['mapRef'], lun=lun_map['lun']))
    else:
        post_body = json.dumps(dict(mappableObjectId=lun_map['volumeRef'], targetId=lun_map['mapRef']))
    (rc, data) = request(url, data=post_body, method='POST', url_username=user, url_password=pwd, headers=HEADERS, ignore_errors=True, validate_certs=validate_certs)
    if ((rc == 422) and (lun_map['lun'] is not None)):
        data = move_lun(module, ssid, lun_map, vol_name, api_url, user, pwd, validate_certs)
    return data