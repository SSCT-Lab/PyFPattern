def delete_host(module, array):
    changed = True
    if (not module.check_mode):
        for vol in array.list_host_connections(module.params['host']):
            array.disconnect_host(module.params['host'], vol['vol'])
        array.delete_host(module.params['host'])
    module.exit_json(changed=changed)