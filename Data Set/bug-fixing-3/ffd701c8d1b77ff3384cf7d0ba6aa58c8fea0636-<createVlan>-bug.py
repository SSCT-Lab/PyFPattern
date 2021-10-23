def createVlan(obj, deviceType, prompt, timeout, vlanArg1, vlanArg2, vlanArg3, vlanArg4, vlanArg5):
    command = (('vlan ' + vlanArg1) + '\n')
    retVal = waitForDeviceResponse(command, prompt, timeout, obj)
    command = ''
    if (vlanArg2 == 'name'):
        command = (vlanArg2 + ' ')
        value = checkSanityofVariable(deviceType, 'vlan_name', vlanArg3)
        if (value == 'ok'):
            value = checkVlanNameNotAssigned(obj, deviceType, prompt, timeout, vlanArg1, vlanArg3)
            if (value == 'ok'):
                command = (command + vlanArg3)
            else:
                command = '\n'
        else:
            retVal = 'Error-139'
            return retVal
    elif (vlanArg2 == 'flood'):
        command = (vlanArg2 + ' ')
        value = checkSanityofVariable(deviceType, 'vlan_flood', vlanArg3)
        if (value == 'ok'):
            command = (command + vlanArg3)
        else:
            retVal = 'Error-140'
            return retVal
    elif (vlanArg2 == 'state'):
        command = (vlanArg2 + ' ')
        value = checkSanityofVariable(deviceType, 'vlan_state', vlanArg3)
        if (value == 'ok'):
            command = (command + vlanArg3)
        else:
            retVal = 'Error-141'
            return retVal
    elif (vlanArg2 == 'ip'):
        command = (vlanArg2 + ' igmp snooping ')
        if ((vlanArg3 is None) or (vlanArg3 == '')):
            command = command
        elif (vlanArg3 == 'fast-leave'):
            command = (command + vlanArg3)
        elif (vlanArg3 == 'last-member-query-interval'):
            command = ((command + vlanArg3) + ' ')
            value = checkSanityofVariable(deviceType, 'vlan_last_member_query_interval', vlanArg4)
            if (value == 'ok'):
                command = (command + vlanArg4)
            else:
                retVal = 'Error-142'
                return retVal
        elif (vlanArg3 == 'querier'):
            command = ((command + vlanArg3) + ' ')
            value = checkSanityofVariable(deviceType, 'vlan_querier', vlanArg4)
            if (value == 'ok'):
                command = (command + vlanArg4)
            else:
                retVal = 'Error-143'
                return retVal
        elif (vlanArg3 == 'querier-timeout'):
            command = ((command + vlanArg3) + ' ')
            value = checkSanityofVariable(deviceType, 'vlan_querier_timeout', vlanArg4)
            if (value == 'ok'):
                command = (command + vlanArg4)
            else:
                retVal = 'Error-144'
                return retVal
        elif (vlanArg3 == 'query-interval'):
            command = ((command + vlanArg3) + ' ')
            value = checkSanityofVariable(deviceType, 'vlan_query_interval', vlanArg4)
            if (value == 'ok'):
                command = (command + vlanArg4)
            else:
                retVal = 'Error-145'
                return retVal
        elif (vlanArg3 == 'query-max-response-time'):
            command = ((command + vlanArg3) + ' ')
            value = checkSanityofVariable(deviceType, 'vlan_query_max_response_time', vlanArg4)
            if (value == 'ok'):
                command = (command + vlanArg4)
            else:
                retVal = 'Error-146'
                return retVal
        elif (vlanArg3 == 'report-suppression'):
            command = (command + vlanArg3)
        elif (vlanArg3 == 'robustness-variable'):
            command = ((command + vlanArg3) + ' ')
            value = checkSanityofVariable(deviceType, 'vlan_robustness_variable', vlanArg4)
            if (value == 'ok'):
                command = (command + vlanArg4)
            else:
                retVal = 'Error-147'
                return retVal
        elif (vlanArg3 == 'startup-query-count'):
            command = ((command + vlanArg3) + ' ')
            value = checkSanityofVariable(deviceType, 'vlan_startup_query_count', vlanArg4)
            if (value == 'ok'):
                command = (command + vlanArg4)
            else:
                retVal = 'Error-148'
                return retVal
        elif (vlanArg3 == 'startup-query-interval'):
            command = ((command + vlanArg3) + ' ')
            value = checkSanityofVariable(deviceType, 'vlan_startup_query_interval', vlanArg4)
            if (value == 'ok'):
                command = (command + vlanArg4)
            else:
                retVal = 'Error-149'
                return retVal
        elif (vlanArg3 == 'static-group'):
            retVal = 'Error-102'
            return retVal
        elif (vlanArg3 == 'version'):
            command = ((command + vlanArg3) + ' ')
            value = checkSanityofVariable(deviceType, 'vlan_snooping_version', vlanArg4)
            if (value == 'ok'):
                command = (command + vlanArg4)
            else:
                retVal = 'Error-150'
                return retVal
        elif (vlanArg3 == 'mrouter'):
            command = ((command + vlanArg3) + ' interface ')
            if (vlanArg4 == 'ethernet'):
                command = ((command + vlanArg4) + ' ')
                value = checkSanityofVariable(deviceType, 'vlan_ethernet_interface', vlanArg5)
                if (value == 'ok'):
                    command = (command + vlanArg5)
                else:
                    retVal = 'Error-151'
                    return retVal
            elif (vlanArg4 == 'port-aggregation'):
                command = ((command + vlanArg4) + ' ')
                value = checkSanityofVariable(deviceType, 'vlan_portagg_number', vlanArg5)
                if (value == 'ok'):
                    command = (command + vlanArg5)
                else:
                    retVal = 'Error-152'
                    return retVal
            else:
                retVal = 'Error-153'
                return retVal
        else:
            command = (command + vlanArg3)
    else:
        retVal = 'Error-154'
        return retVal
    command = (command + '\n')
    retVal = ((retVal + '\n') + waitForDeviceResponse(command, prompt, timeout, obj))
    command = 'exit \n'
    retVal = (retVal + waitForDeviceResponse(command, '(config)#', timeout, obj))
    return retVal