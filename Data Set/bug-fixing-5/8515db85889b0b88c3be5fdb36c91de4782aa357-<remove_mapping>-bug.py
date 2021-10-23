def remove_mapping(module, ssid, lun_mapping, api_url, user, pwd):
    lun_id = get_lun_id(module, ssid, lun_mapping, api_url, user, pwd)
    lun_del = ('storage-systems/%s/volume-mappings/%s' % (ssid, lun_id))
    url = (api_url + lun_del)
    (rc, data) = request(url, method='DELETE', url_username=user, url_password=pwd, headers=HEADERS)
    return data