def _set_host_personality(module, array):
    'Set host personality. Only called when AC is supported'
    array.set_host(module.params['host'], personality=module.params['personality'])