def _update_host_personality(module, array, answer=False):
    'Change host personality. Only called when supported'
    personality = array.get_host(module.params['host'], personality=True)['personality']
    if ((personality is None) and (module.params['personality'] != 'delete')):
        array.set_host(module.params['host'], personality=module.params['personality'])
        answer = True
    if (personality is not None):
        if (module.params['personality'] == 'delete'):
            array.set_host(module.params['host'], personality='')
            answer = True
        elif (personality != module.params['personality']):
            array.set_host(module.params['host'], personality=module.params['personality'])
            answer = True
    return answer