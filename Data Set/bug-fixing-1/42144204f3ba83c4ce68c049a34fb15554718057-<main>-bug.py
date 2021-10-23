

def main():
    argument_spec = purefa_argument_spec()
    argument_spec.update(dict(host=dict(type='str', required=True), state=dict(type='str', default='present', choices=['absent', 'present']), protocol=dict(type='str', default='iscsi', choices=['fc', 'iscsi', 'nvme', 'mixed']), nqn=dict(type='list'), iqn=dict(type='list'), wwns=dict(type='list'), volume=dict(type='str'), lun=dict(type='int'), personality=dict(type='str', default='', choices=['hpux', 'vms', 'aix', 'esxi', 'solaris', 'hitachi-vsp', 'oracle-vm-server', 'delete', '']), preferred_array=dict(type='list')))
    module = AnsibleModule(argument_spec, supports_check_mode=True)
    array = get_system(module)
    if ((_is_cbs(module, array) and module.params['wwns']) or module.params['nqn']):
        module.fail_json(msg='Cloud block Store only support iSCSI as a protocol')
    api_version = array._list_available_rest_versions()
    if ((module.params['nqn'] is not None) and (NVME_API_VERSION not in api_version)):
        module.fail_json(msg='NVMe protocol not supported. Please upgrade your array.')
    state = module.params['state']
    host = get_host(module, array)
    if (module.params['lun'] and (not (1 <= module.params['lun'] <= 4095))):
        module.fail_json(msg='LUN ID of {0} is out of range (1 to 4095)'.format(module.params['lun']))
    if module.params['volume']:
        try:
            array.get_volume(module.params['volume'])
        except Exception:
            module.fail_json(msg='Volume {0} not found'.format(module.params['volume']))
    if module.params['preferred_array']:
        try:
            if (module.params['preferred_array'] != ['delete']):
                all_connected_arrays = array.list_array_connections()
                if (not all_connected_arrays):
                    module.fail_json(msg='No target arrays connected to source array. Setting preferred arrays not possible.')
                else:
                    current_arrays = []
                    for current_array in range(0, len(all_connected_arrays)):
                        current_arrays.append(all_connected_arrays[current_array]['array_name'])
                for array_to_connect in range(0, len(module.params['preferred_array'])):
                    if (module.params['preferred_array'][array_to_connect] not in current_arrays):
                        module.fail_json(msg='Array {0} not in existing array connections.'.format(module.params['preferred_array'][array_to_connect]))
        except Exception:
            module.fail_json(msg='Failed to get existing array connections.')
    if ((host is None) and (state == 'present')):
        make_host(module, array)
    elif (host and (state == 'present')):
        update_host(module, array)
    elif (host and (state == 'absent')):
        delete_host(module, array)
    elif ((host is None) and (state == 'absent')):
        module.exit_json(changed=False)
