def doRunningConfigBackUp(protocol, timeout, confServerIp, confPath, confServerUser, confServerPwd, obj):
    server = confServerIp
    username = confServerUser
    password = confServerPwd
    if ((confPath is None) or (confPath is '')):
        confPath = 'cnos_config'
    retVal = ''
    if (protocol == 'ftp'):
        command = (((((((((('cp running-config ' + protocol) + ' ') + protocol) + '://') + username) + '@') + server) + '/') + confPath) + ' vrf management\n')
        retVal = (retVal + waitForDeviceResponse(command, 'Password:', 3, obj))
        retVal = (retVal + waitForDeviceResponse(password, '#', timeout, obj))
    elif (protocol == 'tftp'):
        command = (((((((('cp running-config ' + protocol) + ' ') + protocol) + '://') + server) + '/') + confPath) + ' vrf management\n')
        retVal = (retVal + waitForDeviceResponse(command, '#', 3, obj))
    else:
        return 'Error-110'
    return retVal