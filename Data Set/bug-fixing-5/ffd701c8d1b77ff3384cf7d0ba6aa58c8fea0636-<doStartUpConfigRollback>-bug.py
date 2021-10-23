def doStartUpConfigRollback(protocol, timeout, confServerIp, confPath, confServerUser, confServerPwd, obj):
    server = confServerIp
    username = confServerUser
    password = confServerPwd
    path = 'cnos_config'
    if ((confPath is not None) & (confPath != '')):
        path = confPath
    retVal = ''
    if (protocol == 'ftp'):
        command = (((((((((('cp ' + protocol) + ' ') + protocol) + '://') + username) + '@') + server) + '/') + path) + ' startup-config vrf management\n')
        retVal = (retVal + waitForDeviceResponse(command, 'Password:', 3, obj))
        retVal = (retVal + waitForDeviceResponse(command, '[n]', timeout, obj))
        command = 'y\n'
        retVal = (retVal + waitForDeviceResponse(password, '#', timeout, obj))
    elif (protocol == 'tftp'):
        command = (((((((('cp ' + protocol) + ' ') + protocol) + '://') + server) + '/') + path) + ' startup-config vrf management\n')
        retVal = (retVal + waitForDeviceResponse(command, '[n]', timeout, obj))
        command = 'y\n'
        retVal = (retVal + waitForDeviceResponse(command, '#', timeout, obj))
    else:
        return 'Error-110'
    return retVal