def delete_host(module, array):
    changed = False
    try:
        for vol in array.list_host_connections(module.params['host']):
            array.disconnect_host(module.params['host'], vol['vol'])
        array.delete_host(module.params['host'])
        changed = True
    except:
        module.fail_json(msg='Host {0} deletion failed'.format(module.params['host']))
    module.exit_json(changed=changed)