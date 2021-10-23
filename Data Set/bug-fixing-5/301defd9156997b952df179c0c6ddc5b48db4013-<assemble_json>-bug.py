def assemble_json(cpmmodule):
    json_load = ''
    json_load = '{"users":'
    json_load = (((json_load + '{"username": "') + cpmmodule.params['user_name']) + '"')
    if ((cpmmodule.params['user_pass'] is not None) and (len(cpmmodule.params['user_pass']) > 0)):
        json_load = (((json_load + ',"newpasswd": "') + cpmmodule.params['user_pass']) + '"')
    if (cpmmodule.params['user_accesslevel'] is not None):
        json_load = (((json_load + ',"accesslevel": ') + str(cpmmodule.params['user_accesslevel'])) + '')
    if (cpmmodule.params['user_portaccess'] is not None):
        json_load = (((json_load + ',"portaccess": ') + cpmmodule.params['user_portaccess']) + '')
    if (cpmmodule.params['user_plugaccess'] is not None):
        json_load = (((json_load + ',"plugaccess": ') + cpmmodule.params['user_plugaccess']) + '')
    if (cpmmodule.params['user_groupaccess'] is not None):
        json_load = (((json_load + ',"groupaccess": ') + cpmmodule.params['user_groupaccess']) + '')
    if (cpmmodule.params['user_accessserial'] is not None):
        json_load = (((json_load + ',"accessserial": ') + str(cpmmodule.params['user_accessserial'])) + '')
    if (cpmmodule.params['user_accessssh'] is not None):
        json_load = (((json_load + ',"accessssh": ') + str(cpmmodule.params['user_accessssh'])) + '')
    if (cpmmodule.params['user_accessweb'] is not None):
        json_load = (((json_load + ',"accessweb": ') + str(cpmmodule.params['user_accessweb'])) + '')
    if (cpmmodule.params['user_accessoutbound'] is not None):
        json_load = (((json_load + ',"accessoutbound": ') + str(cpmmodule.params['user_accessoutbound'])) + '')
    if (cpmmodule.params['user_accessapi'] is not None):
        json_load = (((json_load + ',"accessapi": ') + str(cpmmodule.params['user_accessapi'])) + '')
    if (cpmmodule.params['user_accessmonitor'] is not None):
        json_load = (((json_load + ',"accessmonitor": ') + str(cpmmodule.params['user_accessmonitor'])) + '')
    if (cpmmodule.params['user_callbackphone'] is not None):
        json_load = (((json_load + ',"callbackphone": "') + cpmmodule.params['user_callbackphone']) + '"')
    json_load = (json_load + '}')
    json_load = (json_load + '}')
    return json_load