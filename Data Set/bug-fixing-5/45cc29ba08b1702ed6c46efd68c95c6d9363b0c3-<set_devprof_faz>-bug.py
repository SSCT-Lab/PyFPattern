def set_devprof_faz(fmgr, paramgram):
    '\n    :param fmgr: The fmgr object instance from fortimanager.py\n    :type fmgr: class object\n    :param paramgram: The formatted dictionary of options to process\n    :type paramgram: dict\n    :return: The response from the FortiManager\n    :rtype: dict\n    '
    paramgram['mode'] = paramgram['mode']
    adom = paramgram['adom']
    response = DEFAULT_RESULT_OBJ
    datagram = {
        'target-ip': paramgram['admin_fortianalyzer_target'],
        'target': 4,
    }
    url = '/pm/config/adom/{adom}/devprof/{provisioning_template}/device/profile/fortianalyzer'.format(adom=adom, provisioning_template=paramgram['provisioning_template'])
    if (paramgram['mode'] == 'delete'):
        datagram['hastarget'] = 'True'
    response = fmgr.process_request(url, datagram, paramgram['mode'])
    return response