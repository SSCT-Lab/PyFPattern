def main():
    argument_spec = eseries_host_argument_spec()
    argument_spec.update(dict(state=dict(required=True, choices=['present', 'absent']), target=dict(required=False, default=None), target_type=dict(required=False, choices=['host', 'group']), lun=dict(required=False, type='int'), volume_name=dict(required=True)))
    module = AnsibleModule(argument_spec=argument_spec)
    state = module.params['state']
    target = module.params['target']
    target_type = module.params['target_type']
    lun = module.params['lun']
    ssid = module.params['ssid']
    validate_certs = module.params['validate_certs']
    vol_name = module.params['volume_name']
    user = module.params['api_username']
    pwd = module.params['api_password']
    api_url = module.params['api_url']
    if (not api_url.endswith('/')):
        api_url += '/'
    volume_map = get_volumes(module, ssid, api_url, user, pwd, 'volumes', validate_certs)
    thin_volume_map = get_volumes(module, ssid, api_url, user, pwd, 'thin-volumes', validate_certs)
    volref = None
    for vol in volume_map:
        if (vol['label'] == vol_name):
            volref = vol['volumeRef']
    if (not volref):
        for vol in thin_volume_map:
            if (vol['label'] == vol_name):
                volref = vol['volumeRef']
    if (not volref):
        module.fail_json(changed=False, msg=('No volume with the name %s was found' % vol_name))
    host_and_group_mapping = get_host_and_group_map(module, ssid, api_url, user, pwd, validate_certs)
    desired_lun_mapping = dict(mapRef=host_and_group_mapping[target_type][target], lun=lun, volumeRef=volref)
    lun_mappings = get_lun_mappings(ssid, api_url, user, pwd, validate_certs)
    if (state == 'present'):
        if (desired_lun_mapping in lun_mappings):
            module.exit_json(changed=False, msg='Mapping exists')
        else:
            result = create_mapping(module, ssid, desired_lun_mapping, vol_name, api_url, user, pwd, validate_certs)
            module.exit_json(changed=True, **result)
    elif (state == 'absent'):
        if (desired_lun_mapping in lun_mappings):
            result = remove_mapping(module, ssid, desired_lun_mapping, api_url, user, pwd, validate_certs)
            module.exit_json(changed=True, msg='Mapping removed')
        else:
            module.exit_json(changed=False, msg='Mapping absent')