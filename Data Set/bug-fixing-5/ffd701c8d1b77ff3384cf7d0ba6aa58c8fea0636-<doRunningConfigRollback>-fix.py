def doRunningConfigRollback(protocol, timeout, confServerIp, confPath, confServerUser, confServerPwd, obj):
    server = confServerIp
    username = confServerUser
    password = confServerPwd
    if ((confPath is None) or (confPath is '')):
        confPath = 'cnos_config'
    retVal = ''
    if (protocol == 'ftp'):
        command = (((((((((('cp ' + protocol) + ' ') + protocol) + '://') + username) + '@') + server) + '/') + confPath) + ' running-config vrf management\n')
        retVal = (retVal + waitForDeviceResponse(command, 'Password:', 3, obj))
        retVal = (retVal + waitForDeviceResponse(password, '#', timeout, obj))
    elif (protocol == 'tftp'):
        command = (((((((('cp ' + protocol) + ' ') + protocol) + '://') + server) + '/') + confPath) + ' running-config vrf management\n')
        retVal = (retVal + waitForDeviceResponse(command, '#', timeout, obj))
    else:
        return 'Error-110'
    return retVal