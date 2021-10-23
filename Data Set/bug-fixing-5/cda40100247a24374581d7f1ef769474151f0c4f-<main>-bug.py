def main():
    argument_spec = purefa_argument_spec()
    argument_spec.update(dict(host=dict(type='str', required=True), state=dict(type='str', default='present', choices=['absent', 'present']), protocol=dict(type='str', default='iscsi', choices=['fc', 'iscsi', 'nvmef', 'mixed']), nqn=dict(type='list'), iqn=dict(type='list'), wwns=dict(type='list'), volume=dict(type='str'), lun=dict(type='int'), personality=dict(type='str', default='', choices=['hpux', 'vms', 'aix', 'esxi', 'solaris', 'hitachi-vsp', 'oracle-vm-server', 'delete', ''])))
    module = AnsibleModule(argument_spec, supports_check_mode=False)
    if (not HAS_PURESTORAGE):
        module.fail_json(msg='purestorage sdk is required for this module in host')
    api_version = array._list_available_rest_versions()
    if ((module.params['nqn'] is not None) and (NVMEF_API_VERSION not in api_version)):
        module.fail_json(msg='NVMeF protocol not supported. Please upgrade your array.')
    state = module.params['state']
    protocol = module.params['protocol']
    array = get_system(module)
    host = get_host(module, array)
    if (module.params['lun'] and (not (1 <= module.params['lun'] <= 4095))):
        module.fail_json(msg='LUN ID of {0} is out of range (1 to 4095)'.format(module.params['lun']))
    if module.params['volume']:
        try:
            array.get_volume(module.params['volume'])
        except Exception:
            module.fail_json(msg='Volume {} not found'.format(module.params['volume']))
    if ((host is None) and (state == 'present')):
        make_host(module, array)
    elif (host and (state == 'present')):
        update_host(module, array)
    elif (host and (state == 'absent')):
        delete_host(module, array)
    elif ((host is None) and (state == 'absent')):
        module.exit_json(changed=False)