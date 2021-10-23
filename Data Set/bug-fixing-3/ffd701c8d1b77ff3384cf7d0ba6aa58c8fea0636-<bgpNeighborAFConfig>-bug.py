def bgpNeighborAFConfig(obj, deviceType, prompt, timeout, bgpNeighborAFArg1, bgpNeighborAFArg2, bgpNeighborAFArg3):
    retVal = ''
    command = ''
    timeout = timeout
    if (bgpNeighborAFArg1 == 'allowas-in'):
        command = ((command + bgpNeighborAFArg1) + ' ')
        if (bgpNeighborAFArg2 is not None):
            value = checkSanityofVariable(deviceType, 'bgp_neighbor_af_occurances', bgpNeighborAFArg2)
            if (value == 'ok'):
                command = (command + bgpNeighborAFArg2)
            else:
                retVal = 'Error-325'
                return retVal
        else:
            command = command
    elif (bgpNeighborAFArg1 == 'default-originate'):
        command = ((command + bgpNeighborAFArg1) + ' ')
        if ((bgpNeighborAFArg2 is not None) and (bgpNeighborAFArg2 == 'route-map')):
            command = ((command + bgpNeighborAFArg2) + ' ')
            value = checkSanityofVariable(deviceType, 'bgp_neighbor_af_routemap', bgpNeighborAFArg2)
            if (value == 'ok'):
                command = (command + bgpNeighborAFArg3)
            else:
                retVal = 'Error-324'
                return retVal
    elif (bgpNeighborAFArg1 == 'filter-list'):
        command = ((command + bgpNeighborAFArg1) + ' ')
        value = checkSanityofVariable(deviceType, 'bgp_neighbor_af_filtername', bgpNeighborAFArg2)
        if (value == 'ok'):
            command = ((command + bgpNeighborAFArg2) + ' ')
            if ((bgpNeighborAFArg3 == 'in') or (bgpNeighborAFArg3 == 'out')):
                command = (command + bgpNeighborAFArg3)
            else:
                retVal = 'Error-323'
                return retVal
        else:
            retVal = 'Error-322'
            return retVal
    elif (bgpNeighborAFArg1 == 'maximum-prefix'):
        command = ((command + bgpNeighborAFArg1) + ' ')
        value = checkSanityofVariable(deviceType, 'bgp_neighbor_af_maxprefix', bgpNeighborAFArg2)
        if (value == 'ok'):
            command = ((command + bgpNeighborAFArg2) + ' ')
            if (bgpNeighborAFArg3 is not None):
                command = (command + bgpNeighborAFArg3)
            else:
                command = command
        else:
            retVal = 'Error-326'
            return retVal
    elif (bgpNeighborAFArg1 == 'next-hop-self'):
        command = (command + bgpNeighborAFArg1)
    elif (bgpNeighborAFArg1 == 'prefix-list'):
        command = ((command + bgpNeighborAFArg1) + ' ')
        value = checkSanityofVariable(deviceType, 'bgp_neighbor_af_prefixname', bgpNeighborAFArg2)
        if (value == 'ok'):
            command = ((command + bgpNeighborAFArg2) + ' ')
            if ((bgpNeighborAFArg3 == 'in') or (bgpNeighborAFArg3 == 'out')):
                command = (command + bgpNeighborAFArg3)
            else:
                retVal = 'Error-321'
                return retVal
        else:
            retVal = 'Error-320'
            return retVal
    elif (bgpNeighborAFArg1 == 'route-map'):
        command = ((command + bgpNeighborAFArg1) + ' ')
        value = checkSanityofVariable(deviceType, 'bgp_neighbor_af_routemap', bgpNeighborAFArg2)
        if (value == 'ok'):
            command = (command + bgpNeighborAFArg2)
        else:
            retVal = 'Error-319'
            return retVal
    elif (bgpNeighborAFArg1 == 'route-reflector-client'):
        command = (command + bgpNeighborAFArg1)
    elif (bgpNeighborAFArg1 == 'send-community'):
        command = ((command + bgpNeighborAFArg1) + ' ')
        if ((bgpNeighborAFArg2 is not None) and (bgpNeighborAFArg2 == 'extended')):
            command = (command + bgpNeighborAFArg2)
        else:
            command = command
    elif (bgpNeighborAFArg1 == 'soft-reconfiguration'):
        command = ((command + bgpNeighborAFArg1) + ' inbound')
    elif (bgpNeighborAFArg1 == 'unsuppress-map'):
        command = ((command + bgpNeighborAFArg1) + ' ')
        value = checkSanityofVariable(deviceType, 'bgp_neighbor_af_routemap', bgpNeighborAFArg2)
        if (value == 'ok'):
            command = (command + bgpNeighborAFArg2)
        else:
            retVal = 'Error-318'
            return retVal
    else:
        retVal = 'Error-317'
        return retVal
    command = (command + '\n')
    retVal = (retVal + waitForDeviceResponse(command, prompt, timeout, obj))
    command = 'exit \n'
    retVal = (retVal + waitForDeviceResponse(command, '(config-router-neighbor)#', timeout, obj))
    return retVal