def doStartupConfigBackUp(protocol, timeout, confServerIp, confPath, confServerUser, confServerPwd, obj):
    server = confServerIp
    username = confServerUser
    password = confServerPwd
    path = 'cnos_config'
    if ((confPath is not None) & (confPath != '')):
        path = confPath
    retVal = ''
    if (protocol == 'ftp'):
        command = (((((((((('cp startup-config ' + protocol) + ' ') + protocol) + '://') + username) + '@') + server) + '/') + path) + ' vrf management\n')
        retVal = (retVal + waitForDeviceResponse(command, 'Password:', 3, obj))
        retVal = (retVal + waitForDeviceResponse(password, '#', timeout, obj))
    elif (protocol == 'tftp'):
        command = (((((((('cp startup-config ' + protocol) + ' ') + protocol) + '://') + server) + '/') + path) + ' vrf management\n')
        retVal = (retVal + waitForDeviceResponse(command, '#', 3, obj))
    else:
        return 'Error-110'
    return retVal