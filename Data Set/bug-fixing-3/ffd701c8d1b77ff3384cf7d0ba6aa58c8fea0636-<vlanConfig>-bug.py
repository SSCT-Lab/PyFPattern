def vlanConfig(obj, deviceType, prompt, timeout, vlanArg1, vlanArg2, vlanArg3, vlanArg4, vlanArg5):
    retVal = ''
    timeout = timeout
    command = 'vlan '
    if (vlanArg1 == 'access-map'):
        command = ((command + vlanArg1) + ' ')
        value = checkSanityofVariable(deviceType, 'vlan_access_map_name', vlanArg2)
        if (value == 'ok'):
            command = ((command + vlanArg2) + ' \n')
            retVal = waitForDeviceResponse(command, '(config-access-map)#', timeout, obj)
            retVal = (retVal + vlanAccessMapConfig(obj, deviceType, '(config-access-map)#', timeout, vlanArg3, vlanArg4, vlanArg5))
            return retVal
        else:
            retVal = 'Error-130'
            return retVal
    elif (vlanArg1 == 'dot1q'):
        command = ((command + vlanArg1) + ' tag native ')
        if (vlanArg2 is not None):
            value = checkSanityofVariable(deviceType, 'vlan_dot1q_tag', vlanArg2)
            if (value == 'ok'):
                command = (command + vlanArg2)
            else:
                retVal = 'Error-131'
                return retVal
    elif (vlanArg1 == 'filter'):
        command = ((command + vlanArg1) + ' ')
        if (vlanArg2 is not None):
            value = checkSanityofVariable(deviceType, 'vlan_filter_name', vlanArg2)
            if (value == 'ok'):
                command = ((command + vlanArg2) + ' vlan-list ')
                value = checkSanityofVariable(deviceType, 'vlan_id', vlanArg3)
                if (value == 'ok'):
                    command = (command + vlanArg3)
                else:
                    value = checkSanityofVariable(deviceType, 'vlan_id_range', vlanArg3)
                    if (value == 'ok'):
                        command = (command + vlanArg3)
                    else:
                        retVal = 'ERROR-133'
                    return retVal
            else:
                retVal = 'Error-132'
                return retVal
    else:
        value = checkSanityofVariable(deviceType, 'vlan_id', vlanArg1)
        if (value == 'ok'):
            retVal = createVlan(obj, deviceType, '(config-vlan)#', timeout, vlanArg1, vlanArg2, vlanArg3, vlanArg4, vlanArg5)
            return retVal
        else:
            value = checkSanityofVariable(deviceType, 'vlan_id_range', vlanArg1)
            if (value == 'ok'):
                retVal = createVlan(obj, deviceType, '(config-vlan)#', timeout, vlanArg1, vlanArg2, vlanArg3, vlanArg4, vlanArg5)
                return retVal
            retVal = 'Error-133'
            return retVal
        retVal = 'Error-134'
        return retVal
    command = (command + '\n')
    retVal = (retVal + waitForDeviceResponse(command, prompt, timeout, obj))
    return retVal