def doImageTransfer(protocol, timeout, imgServerIp, imgPath, imgType, imgServerUser, imgServerPwd, obj):
    server = imgServerIp
    username = imgServerUser
    password = imgServerPwd
    type = 'os'
    if (imgType is not None):
        type = imgType.lower()
    path = 'cnos_images'
    if ((imgPath is not None) and (imgPath != '')):
        path = imgPath
    retVal = ''
    if (protocol == 'ftp'):
        command = (((((((((((('cp ' + protocol) + ' ') + protocol) + '://') + username) + '@') + server) + '/') + path) + ' system-image ') + type) + ' vrf management\n')
    elif (protocol == 'tftp'):
        command = (((((((((('cp ' + protocol) + ' ') + protocol) + '://') + server) + '/') + path) + ' system-image ') + type) + ' vrf management\n')
    else:
        return 'Error-110'
    retVal = (retVal + waitForDeviceResponse(command, '[n]', 3, obj))
    command = 'y\n'
    if (protocol == 'ftp'):
        retVal = (retVal + waitForDeviceResponse(command, 'Password:', 3, obj))
        command = (password + ' \n')
    retVal = (retVal + waitForDeviceResponse(command, '[n]', timeout, obj))
    command = 'y\n'
    retVal = (retVal + waitForDeviceResponse(command, '#', timeout, obj))
    return retVal