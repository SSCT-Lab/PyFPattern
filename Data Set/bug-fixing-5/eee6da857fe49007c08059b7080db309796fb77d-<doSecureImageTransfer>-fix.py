def doSecureImageTransfer(protocol, timeout, imgServerIp, imgPath, imgType, imgServerUser, imgServerPwd, obj):
    server = imgServerIp
    username = imgServerUser
    password = imgServerPwd
    type = 'scp'
    if (imgType is not None):
        type = imgType.lower()
    if ((imgPath is None) or (imgPath is '')):
        imgPath = 'cnos_images'
    retVal = ''
    command = (((((((((((('cp ' + protocol) + ' ') + protocol) + '://') + username) + '@') + server) + '/') + imgPath) + ' system-image ') + type) + ' vrf management \n')
    response = waitForDeviceResponse(command, '[n]', 3, obj)
    if response.lower().find('error-101'):
        retVal = retVal
    else:
        retVal = (retVal + response)
    if (protocol == 'scp'):
        command = 'y\n'
        response = waitForDeviceResponse(command, '(yes/no)?', 3, obj)
        if response.lower().find('error-101'):
            retVal = retVal
        else:
            retVal = (retVal + response)
        command = 'Yes\n'
        retVal = (retVal + waitForDeviceResponse(command, 'timeout:', 3, obj))
        command = '0\n'
        retVal = (retVal + waitForDeviceResponse(command, 'Password:', 3, obj))
    elif (protocol == 'sftp'):
        command = 'y\n'
        response = waitForDeviceResponse(command, '(yes/no)?', 3, obj)
        if response.lower().find('error-101'):
            retVal = retVal
        else:
            retVal = (retVal + response)
        command = 'Yes\n'
        retVal = (retVal + waitForDeviceResponse(command, 'Password:', 3, obj))
    else:
        return 'Error-110'
    command = (password + '\n')
    retVal = (retVal + waitForDeviceResponse(command, '[n]', timeout, obj))
    command = 'y\n'
    retVal = (retVal + waitForDeviceResponse(command, '#', timeout, obj))
    return retVal