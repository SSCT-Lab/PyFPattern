def move_lun(module, ssid, lun_map, vol_name, api_url, user, pwd):
    lun_id = get_lun_id(module, ssid, lun_map, api_url, user, pwd)
    move_lun = ('storage-systems/%s/volume-mappings/%s/move' % (ssid, lun_id))
    url = (api_url + move_lun)
    post_body = json.dumps(dict(targetId=lun_map['mapRef'], lun=lun_map['lun']))
    (rc, data) = request(url, data=post_body, method='POST', url_username=user, url_password=pwd, headers=HEADERS)
    return data