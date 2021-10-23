def doImageTransfer(protocol, timeout, imgServerIp, imgPath, imgType, imgServerUser, imgServerPwd, obj):
    server = imgServerIp
    username = imgServerUser
    password = imgServerPwd
    type = 'os'
    if (imgType is not None):
        type = imgType.lower()
    if ((imgPath is None) or (imgPath is '')):
        imgPath = 'cnos_images'
    retVal = ''
    if (protocol == 'ftp'):
        command = (((((((((((('cp ' + protocol) + ' ') + protocol) + '://') + username) + '@') + server) + '/') + imgPath) + ' system-image ') + type) + ' vrf management\n')
    elif (protocol == 'tftp'):
        command = (((((((((('cp ' + protocol) + ' ') + protocol) + '://') + server) + '/') + imgPath) + ' system-image ') + type) + ' vrf management\n')
    else:
        return 'Error-110'
    response = waitForDeviceResponse(command, '[n]', 3, obj)
    if response.lower().find('error-101'):
        retVal = retVal
    else:
        retVal = (retVal + response)
    command = 'y\n'
    if (protocol == 'ftp'):
        retVal = (retVal + waitForDeviceResponse(command, 'Password:', 3, obj))
        command = (password + ' \n')
    retVal = (retVal + waitForDeviceResponse(command, '[n]', timeout, obj))
    command = 'y\n'
    retVal = (retVal + waitForDeviceResponse(command, '#', timeout, obj))
    return retVal