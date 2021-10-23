

def interfaceConfig(obj, deviceType, prompt, timeout, interfaceArg1, interfaceArg2, interfaceArg3, interfaceArg4, interfaceArg5, interfaceArg6, interfaceArg7, interfaceArg8, interfaceArg9):
    retVal = ''
    command = 'interface '
    newPrompt = prompt
    if (interfaceArg1 == 'port-aggregation'):
        command = (((((command + ' ') + interfaceArg1) + ' ') + interfaceArg2) + '\n')
        value = checkSanityofVariable(deviceType, 'portchannel_interface_value', interfaceArg2)
        if (value == 'ok'):
            newPrompt = '(config-if)#'
            retVal = (retVal + waitForDeviceResponse(command, newPrompt, timeout, obj))
        else:
            value = checkSanityofVariable(deviceType, 'portchannel_interface_range', interfaceArg2)
            if (value == 'ok'):
                newPrompt = '(config-if-range)#'
                retVal = (retVal + waitForDeviceResponse(command, newPrompt, timeout, obj))
            else:
                value = checkSanityofVariable(deviceType, 'portchannel_interface_string', interfaceArg2)
                if (value == 'ok'):
                    newPrompt = '(config-if-range)#'
                    if ('/' in interfaceArg2):
                        newPrompt = '(config-if)#'
                    retVal = (retVal + waitForDeviceResponse(command, newPrompt, timeout, obj))
                else:
                    retVal = 'Error-102'
                    return retVal
        retVal = (retVal + interfaceLevel2Config(obj, deviceType, newPrompt, timeout, interfaceArg3, interfaceArg4, interfaceArg5, interfaceArg6, interfaceArg7, interfaceArg8, interfaceArg9))
    elif (interfaceArg1 == 'ethernet'):
        value = checkSanityofVariable(deviceType, 'ethernet_interface_value', interfaceArg2)
        if (value == 'ok'):
            newPrompt = '(config-if)#'
            command = ((((command + interfaceArg1) + ' 1/') + interfaceArg2) + ' \n')
            retVal = (retVal + waitForDeviceResponse(command, newPrompt, timeout, obj))
        else:
            value = checkSanityofVariable(deviceType, 'ethernet_interface_range', interfaceArg2)
            if (value == 'ok'):
                command = ((((command + interfaceArg1) + ' 1/') + interfaceArg2) + ' \n')
                newPrompt = '(config-if-range)#'
                retVal = (retVal + waitForDeviceResponse(command, newPrompt, timeout, obj))
            else:
                value = checkSanityofVariable(deviceType, 'ethernet_interface_string', interfaceArg2)
                if (value == 'ok'):
                    command = ((((command + interfaceArg1) + ' ') + interfaceArg2) + '\n')
                    newPrompt = '(config-if-range)#'
                    if ('/' in interfaceArg2):
                        newPrompt = '(config-if)#'
                    retVal = (retVal + waitForDeviceResponse(command, newPrompt, timeout, obj))
                else:
                    retVal = 'Error-102'
                    return retVal
        retVal = (retVal + interfaceLevel2Config(obj, deviceType, newPrompt, timeout, interfaceArg3, interfaceArg4, interfaceArg5, interfaceArg6, interfaceArg7, interfaceArg8, interfaceArg9))
    elif (interfaceArg1 == 'loopback'):
        value = checkSanityofVariable(deviceType, 'loopback_interface_value', interfaceArg2)
        if (value == 'ok'):
            newPrompt = '(config-if)#'
            command = ((((command + interfaceArg1) + ' ') + interfaceArg2) + '\n')
            retVal = (retVal + waitForDeviceResponse(command, newPrompt, timeout, obj))
        else:
            retVal = 'Error-102'
            return retVal
        retVal = (retVal + interfaceLevel2Config(obj, deviceType, newPrompt, timeout, interfaceArg3, interfaceArg4, interfaceArg5, interfaceArg6, interfaceArg7, interfaceArg8, interfaceArg9))
    elif (interfaceArg1 == 'mgmt'):
        value = checkSanityofVariable(deviceType, 'mgmt_interface_value', interfaceArg2)
        if (value == 'ok'):
            newPrompt = '(config-if)#'
            command = ((((command + interfaceArg1) + ' ') + interfaceArg2) + '\n')
            retVal = (retVal + waitForDeviceResponse(command, newPrompt, timeout, obj))
        else:
            retVal = 'Error-102'
            return retVal
        retVal = (retVal + interfaceLevel2Config(obj, deviceType, newPrompt, timeout, interfaceArg3, interfaceArg4, interfaceArg5, interfaceArg6, interfaceArg7, interfaceArg8, interfaceArg9))
    elif (interfaceArg1 == 'vlan'):
        value = checkSanityofVariable(deviceType, 'vlan_interface_value', interfaceArg2)
        if (value == 'ok'):
            newPrompt = '(config-if)#'
            command = ((((command + interfaceArg1) + ' ') + interfaceArg2) + '\n')
            retVal = (retVal + waitForDeviceResponse(command, newPrompt, timeout, obj))
        else:
            retVal = 'Error-102'
            return retVal
        retVal = (retVal + interfaceLevel2Config(obj, deviceType, newPrompt, timeout, interfaceArg3, interfaceArg4, interfaceArg5, interfaceArg6, interfaceArg7, interfaceArg8, interfaceArg9))
    else:
        retVal = 'Error-102'
    return retVal
