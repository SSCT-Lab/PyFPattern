def doStartUpConfigRollback(protocol, timeout, confServerIp, confPath, confServerUser, confServerPwd, obj):
    server = confServerIp
    username = confServerUser
    password = confServerPwd
    if ((confPath is None) or (confPath is '')):
        confPath = 'cnos_config'
    retVal = ''
    if (protocol == 'ftp'):
        command = (((((((((('cp ' + protocol) + ' ') + protocol) + '://') + username) + '@') + server) + '/') + confPath) + ' startup-config vrf management\n')
        retVal = (retVal + waitForDeviceResponse(command, 'Password:', 3, obj))
        retVal = (retVal + waitForDeviceResponse(command, '[n]', timeout, obj))
        command = 'y\n'
        retVal = (retVal + waitForDeviceResponse(password, '#', timeout, obj))
    elif (protocol == 'tftp'):
        command = (((((((('cp ' + protocol) + ' ') + protocol) + '://') + server) + '/') + confPath) + ' startup-config vrf management\n')
        retVal = (retVal + waitForDeviceResponse(command, '[n]', timeout, obj))
        command = 'y\n'
        retVal = (retVal + waitForDeviceResponse(command, '#', timeout, obj))
    else:
        return 'Error-110'
    return retVal