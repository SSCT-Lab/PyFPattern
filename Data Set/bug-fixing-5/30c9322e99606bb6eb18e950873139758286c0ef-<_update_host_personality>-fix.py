def _update_host_personality(module, array, answer=False):
    'Change host personality. Only called when supported'
    personality = array.get_host(module.params['host'], personality=True)['personality']
    if ((personality is None) and (module.params['personality'] != 'delete')):
        try:
            array.set_host(module.params['host'], personality=module.params['personality'])
            answer = True
        except Exception:
            module.fail_json(msg='Personality setting failed.')
    if (personality is not None):
        if (module.params['personality'] == 'delete'):
            try:
                array.set_host(module.params['host'], personality='')
                answer = True
            except Exception:
                module.fail_json(msg='Personality deletion failed.')
        elif (personality != module.params['personality']):
            try:
                array.set_host(module.params['host'], personality=module.params['personality'])
                answer = True
            except Exception:
                module.fail_json(msg='Personality change failed.')
    return answer