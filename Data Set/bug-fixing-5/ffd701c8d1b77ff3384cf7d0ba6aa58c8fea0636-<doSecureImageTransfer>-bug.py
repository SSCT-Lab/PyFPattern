def doSecureImageTransfer(protocol, timeout, imgServerIp, imgPath, imgType, imgServerUser, imgServerPwd, obj):
    server = imgServerIp
    username = imgServerUser
    password = imgServerPwd
    type = 'scp'
    if (imgType is not None):
        type = imgType.lower()
    path = 'cnos_images'
    if ((imgPath is not None) and (imgPath != '')):
        path = imgPath
    retVal = ''
    command = (((((((((((('cp ' + protocol) + ' ') + protocol) + '://') + username) + '@') + server) + '/') + path) + ' system-image ') + type) + ' vrf management \n')
    retVal = (retVal + waitForDeviceResponse(command, '[n]', 3, obj))
    if (protocol == 'scp'):
        command = 'y\n'
        retVal = (retVal + waitForDeviceResponse(command, '(yes/no)?', 3, obj))
        command = 'Yes\n'
        retVal = (retVal + waitForDeviceResponse(command, 'timeout:', 3, obj))
        command = '0\n'
        retVal = (retVal + waitForDeviceResponse(command, 'Password:', 3, obj))
    elif (protocol == 'sftp'):
        command = 'y\n'
        retVal = (retVal + waitForDeviceResponse(command, '(yes/no)?', 3, obj))
        command = 'Yes\n'
        retVal = (retVal + waitForDeviceResponse(command, 'Password:', 3, obj))
    else:
        return 'Error-110'
    command = (password + '\n')
    retVal = (retVal + waitForDeviceResponse(command, '[n]', timeout, obj))
    command = 'y\n'
    retVal = (retVal + waitForDeviceResponse(command, '#', timeout, obj))
    return retVal