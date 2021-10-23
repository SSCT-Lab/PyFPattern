def get_lun_id(module, ssid, lun_mapping, api_url, user, pwd, validate_certs):
    data = get_lun_mappings(ssid, api_url, user, pwd, validate_certs, get_all=True)
    for lun_map in data:
        if (lun_map['volumeRef'] == lun_mapping['volumeRef']):
            return lun_map['id']
    module.fail_json(msg='No LUN map found.')