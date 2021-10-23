def doSecureRunningConfigBackUp(protocol, timeout, confServerIp, confPath, confServerUser, confServerPwd, obj):
    server = confServerIp
    username = confServerUser
    password = confServerPwd
    path = 'cnos_config'
    if ((confPath is not None) and (confPath != '')):
        path = confPath
    retVal = ''
    command = (((((((((('cp running-config ' + protocol) + ' ') + protocol) + '://') + username) + '@') + server) + '/') + path) + ' vrf management\n')
    response = waitForDeviceResponse(command, '(yes/no)', 3, obj)
    if response.lower().find('error-101'):
        command = (password + '\n')
        retVal = (retVal + waitForDeviceResponse(command, '#', timeout, obj))
        return retVal
    retVal = (retVal + response)
    if (protocol == 'scp'):
        command = 'yes \n'
        retVal = (retVal + waitForDeviceResponse(command, 'timeout:', 3, obj))
        command = '0\n'
        retVal = (retVal + waitForDeviceResponse(command, 'Password:', 3, obj))
    elif (protocol == 'sftp'):
        command = 'yes \n'
        retVal = (retVal + waitForDeviceResponse(command, 'Password:', 3, obj))
    else:
        return 'Error-110'
    command = (password + '\n')
    retVal = (retVal + waitForDeviceResponse(command, '#', timeout, obj))
    return retVal