def doSecureStartUpConfigRollback(protocol, timeout, confServerIp, confPath, confServerUser, confServerPwd, obj):
    server = confServerIp
    username = confServerUser
    password = confServerPwd
    if ((confPath is None) or (confPath is '')):
        confPath = 'cnos_config'
    retVal = ''
    command = (((((((((('cp ' + protocol) + ' ') + protocol) + '://') + username) + '@') + server) + '/') + confPath) + ' startup-config vrf management \n')
    response = waitForDeviceResponse(command, '(yes/no)', 3, obj)
    if response.lower().find('error-101'):
        command = (password + '\n')
        retVal = (retVal + waitForDeviceResponse(command, '[n]', timeout, obj))
        command = 'y\n'
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
    retVal = (retVal + waitForDeviceResponse(command, '[n]', timeout, obj))
    command = 'y\n'
    retVal = (retVal + waitForDeviceResponse(command, '#', timeout, obj))
    return retVal