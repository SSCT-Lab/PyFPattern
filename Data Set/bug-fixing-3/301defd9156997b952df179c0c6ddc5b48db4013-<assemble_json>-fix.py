def assemble_json(cpmmodule):
    json_load = ('{"users":{"username": "%s"' % to_native(cpmmodule.params['user_name']))
    if ((cpmmodule.params['user_pass'] is not None) and (len(cpmmodule.params['user_pass']) > 0)):
        json_load = ('%s,"newpasswd": "%s"' % (json_load, to_native(cpmmodule.params['user_pass'])))
    if (cpmmodule.params['user_accesslevel'] is not None):
        json_load = ('%s,"accesslevel": %s' % (json_load, to_native(cpmmodule.params['user_accesslevel'])))
    if (cpmmodule.params['user_portaccess'] is not None):
        json_load = ('%s,"portaccess": %s' % (json_load, to_native(cpmmodule.params['user_portaccess'])))
    if (cpmmodule.params['user_plugaccess'] is not None):
        json_load = ('%s,"plugaccess": %s' % (json_load, to_native(cpmmodule.params['user_plugaccess'])))
    if (cpmmodule.params['user_groupaccess'] is not None):
        json_load = ('%s,"groupaccess": %s' % (json_load, to_native(cpmmodule.params['user_groupaccess'])))
    if (cpmmodule.params['user_accessserial'] is not None):
        json_load = ('%s,"accessserial": %s' % (json_load, to_native(cpmmodule.params['user_accessserial'])))
    if (cpmmodule.params['user_accessssh'] is not None):
        json_load = ('%s,"accessssh": %s' % (json_load, to_native(cpmmodule.params['user_accessssh'])))
    if (cpmmodule.params['user_accessweb'] is not None):
        json_load = ('%s,"accessweb": %s' % (json_load, to_native(cpmmodule.params['user_accessweb'])))
    if (cpmmodule.params['user_accessoutbound'] is not None):
        json_load = ('%s,"accessoutbound": %s' % (json_load, to_native(cpmmodule.params['user_accessoutbound'])))
    if (cpmmodule.params['user_accessapi'] is not None):
        json_load = ('%s,"accessapi": %s' % (json_load, to_native(cpmmodule.params['user_accessapi'])))
    if (cpmmodule.params['user_accessmonitor'] is not None):
        json_load = ('%s,"accessmonitor": %s' % (json_load, to_native(cpmmodule.params['user_accessmonitor'])))
    if (cpmmodule.params['user_callbackphone'] is not None):
        json_load = ('%s,"callbackphone": "%s"' % (json_load, to_native(cpmmodule.params['user_callbackphone'])))
    json_load = ('%s}}' % json_load)
    return json_load