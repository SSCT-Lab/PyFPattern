def set_devprof_scope(fmgr, paramgram):
    '\n    :param fmgr: The fmgr object instance from fortimanager.py\n    :type fmgr: class object\n    :param paramgram: The formatted dictionary of options to process\n    :type paramgram: dict\n    :return: The response from the FortiManager\n    :rtype: dict\n    '
    response = DEFAULT_RESULT_OBJ
    if (paramgram['mode'] in ['set', 'add', 'update']):
        datagram = {
            'name': paramgram['provisioning_template'],
            'type': 'devprof',
            'description': 'CreatedByAnsible',
        }
        targets = []
        for target in paramgram['provision_targets'].split(','):
            new_target = {
                'name': target.strip(),
            }
            targets.append(new_target)
        datagram['scope member'] = targets
        url = '/pm/devprof/adom/{adom}'.format(adom=paramgram['adom'])
    elif (paramgram['mode'] == 'delete'):
        datagram = {
            'name': paramgram['provisioning_template'],
            'type': 'devprof',
            'description': 'CreatedByAnsible',
            'scope member': paramgram['targets_to_add'],
        }
        url = '/pm/devprof/adom/{adom}'.format(adom=paramgram['adom'])
    response = fmgr.process_request(url, datagram, FMGRMethods.SET)
    return response