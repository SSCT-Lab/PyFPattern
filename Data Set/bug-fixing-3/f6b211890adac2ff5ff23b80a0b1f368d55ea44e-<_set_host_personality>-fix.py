def _set_host_personality(module, array):
    'Set host personality. Only called when supported'
    if (module.params['personality'] != 'delete'):
        array.set_host(module.params['host'], personality=module.params['personality'])
    else:
        array.set_host(module.params['host'], personality='')