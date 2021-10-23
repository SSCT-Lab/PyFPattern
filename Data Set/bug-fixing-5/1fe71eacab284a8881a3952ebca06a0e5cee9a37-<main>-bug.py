def main():
    argument_spec = purefa_argument_spec()
    argument_spec.update(dict(host=dict(type='str', required=True), state=dict(type='str', default='present', choices=['absent,present']), protocol=dict(type='str', default='iscsi', choices=['fc', 'iscsi']), iqn=dict(type='list'), wwns=dict(type='list'), volume=dict(type='str')))
    module = AnsibleModule(argument_spec, supports_check_mode=True)
    if (not HAS_PURESTORAGE):
        module.fail_json(msg='purestorage sdk is required for this module in host')
    state = module.params['state']
    protocol = module.params['protocol']
    array = get_system(module)
    host = get_host(module, array)
    if module.params['volume']:
        try:
            array.get_volume(module.params['volume'])
        except:
            module.fail_json(msg='Volume {} not found'.format(module.params['volume']))
    if (host and (state == 'present')):
        update_host(module, array)
    elif (host and (state == 'absent')):
        delete_host(module, array)
    elif ((host is None) and (state == 'absent')):
        module.exit_json(changed=False)
    else:
        make_host(module, array)