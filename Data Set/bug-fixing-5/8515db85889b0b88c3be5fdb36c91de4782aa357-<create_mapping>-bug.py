def create_mapping(module, ssid, lun_map, vol_name, api_url, user, pwd):
    mappings = ('storage-systems/%s/volume-mappings' % ssid)
    url = (api_url + mappings)
    post_body = json.dumps(dict(mappableObjectId=lun_map['volumeRef'], targetId=lun_map['mapRef'], lun=lun_map['lun']))
    (rc, data) = request(url, data=post_body, method='POST', url_username=user, url_password=pwd, headers=HEADERS, ignore_errors=True)
    if (rc == 422):
        data = move_lun(module, ssid, lun_map, vol_name, api_url, user, pwd)
    return data