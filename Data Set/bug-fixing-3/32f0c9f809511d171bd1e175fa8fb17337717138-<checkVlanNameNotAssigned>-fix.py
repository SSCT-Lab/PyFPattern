def checkVlanNameNotAssigned(obj, deviceType, prompt, timeout, vlanId, vlanName):
    retVal = 'ok'
    command = (('display vlan id ' + vlanId) + ' \n')
    retVal = waitForDeviceResponse(command, prompt, timeout, obj)
    if (retVal.find(vlanName) != (- 1)):
        return 'Nok'
    else:
        return 'ok'