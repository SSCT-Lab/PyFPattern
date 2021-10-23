def bgpConfig(obj, deviceType, prompt, timeout, bgpArg1, bgpArg2, bgpArg3, bgpArg4, bgpAgr5, bgpArg6, bgpArg7, bgpArg8):
    retVal = ''
    command = ''
    timeout = timeout
    if (bgpArg1 == 'address-family'):
        command = ((command + bgpArg1) + ' ')
        value = checkSanityofVariable(deviceType, 'bgp_address_family', bgpArg2)
        if (value == 'ok'):
            command = (((command + bgpArg2) + ' ') + 'unicast \n')
            debugOutput(command)
            retVal = waitForDeviceResponse(command, '(config-router-af)#', timeout, obj)
            retVal = (retVal + bgpAFConfig(obj, deviceType, '(config-router-af)#', timeout, bgpArg3, bgpArg4, bgpAgr5, bgpArg6, bgpArg7, bgpArg8))
            return retVal
        else:
            retVal = 'Error-178'
            return retVal
    elif (bgpArg1 == 'bestpath'):
        command = ((command + bgpArg1) + ' ')
        if (bgpArg2 == 'always-compare-med'):
            command = (command + bgpArg2)
        elif (bgpArg2 == 'compare-confed-aspath'):
            command = (command + bgpArg2)
        elif (bgpArg2 == 'compare-routerid'):
            command = (command + bgpArg2)
        elif (bgpArg2 == 'dont-compare-originator-id'):
            command = (command + bgpArg2)
        elif (bgpArg2 == 'tie-break-on-age'):
            command = (command + bgpArg2)
        elif (bgpArg2 == 'as-path'):
            command = ((command + bgpArg2) + ' ')
            if ((bgpArg3 == 'ignore') or (bgpArg3 == 'multipath-relax')):
                command = (command + bgpArg3)
            else:
                retVal = 'Error-179'
                return retVal
        elif (bgpArg2 == 'med'):
            command = ((command + bgpArg2) + ' ')
            if ((bgpArg3 == 'confed') or (bgpArg3 == 'missing-as-worst') or (bgpArg3 == 'non-deterministic') or (bgpArg3 == 'remove-recv-med') or (bgpArg3 == 'remove-send-med')):
                command = (command + bgpArg3)
            else:
                retVal = 'Error-180'
                return retVal
        else:
            retVal = 'Error-181'
            return retVal
    elif (bgpArg1 == 'bgp'):
        command = ((command + bgpArg1) + ' as-local-count ')
        value = checkSanityofVariable(deviceType, 'bgp_bgp_local_count', bgpArg2)
        if (value == 'ok'):
            command = (command + bgpArg2)
        else:
            retVal = 'Error-182'
            return retVal
    elif (bgpArg1 == 'cluster-id'):
        command = ((command + bgpArg1) + ' ')
        value = checkSanityofVariable(deviceType, 'cluster_id_as_ip', bgpArg2)
        if (value == 'ok'):
            command = (command + bgpArg2)
        else:
            value = checkSanityofVariable(deviceType, 'cluster_id_as_number', bgpArg2)
            if (value == 'ok'):
                command = (command + bgpArg2)
            else:
                retVal = 'Error-183'
                return retVal
    elif (bgpArg1 == 'confederation'):
        command = ((command + bgpArg1) + ' ')
        if (bgpArg2 == 'identifier'):
            value = checkSanityofVariable(deviceType, 'confederation_identifier', bgpArg3)
            if (value == 'ok'):
                command = ((((command + ' ') + bgpArg2) + ' ') + bgpArg3)
            else:
                retVal = 'Error-184'
                return retVal
        elif (bgpArg2 == 'peers'):
            value = checkSanityofVariable(deviceType, 'confederation_peers_as', bgpArg3)
            if (value == 'ok'):
                command = ((((command + ' ') + bgpArg2) + ' ') + bgpArg3)
            else:
                retVal = 'Error-185'
                return retVal
        else:
            retVal = 'Error-186'
            return retVal
    elif (bgpArg1 == 'enforce-first-as'):
        command = (command + bgpArg1)
    elif (bgpArg1 == 'fast-external-failover'):
        command = (command + bgpArg1)
    elif (bgpArg1 == 'graceful-restart'):
        command = ((command + bgpArg1) + ' stalepath-time ')
        value = checkSanityofVariable(deviceType, 'stalepath_delay_value', bgpArg2)
        if (value == 'ok'):
            command = (command + bgpArg2)
        else:
            retVal = 'Error-187'
            return retVal
    elif (bgpArg1 == 'graceful-restart-helper'):
        command = (command + bgpArg1)
    elif (bgpArg1 == 'log-neighbor-changes'):
        command = (command + bgpArg1f)
    elif (bgpArg1 == 'maxas-limit'):
        command = ((command + bgpArg1) + ' ')
        value = checkSanityofVariable(deviceType, 'maxas_limit_as', bgpArg2)
        if (value == 'ok'):
            command = (command + bgpArg2)
        else:
            retVal = 'Error-188'
            return retVal
    elif (bgpArg1 == 'neighbor'):
        command = ((command + bgpArg1) + ' ')
        value = checkSanityofVariable(deviceType, 'neighbor_ipaddress', bgpArg2)
        if (value == 'ok'):
            command = (command + bgpArg2)
            if (bgpArg3 is not None):
                command = (command + ' remote-as ')
                value = checkSanityofVariable(deviceType, 'neighbor_as', bgpArg3)
                if (value == 'ok'):
                    command = ((command + bgpArg3) + '\n')
                    retVal = waitForDeviceResponse(command, '(config-router-neighbor)#', timeout, obj)
                    retVal = (retVal + bgpNeighborConfig(obj, deviceType, '(config-router-neighbor)#', timeout, bgpArg4, bgpAgr5, bgpArg6, bgpArg7, bgpArg8))
                    return retVal
        else:
            retVal = 'Error-189'
            return retVal
    elif (bgpArg1 == 'router-id'):
        command = ((command + bgpArg1) + ' ')
        value = checkSanityofVariable(deviceType, 'router_id', bgpArg2)
        if (value == 'ok'):
            command = (command + bgpArg2)
        else:
            retVal = 'Error-190'
            return retVal
    elif (bgpArg1 == 'shutdown'):
        command = (command + bgpArg1)
    elif (bgpArg1 == 'synchronization'):
        command = (command + bgpArg1)
    elif (bgpArg1 == 'timers'):
        command = ((command + bgpArg1) + ' bgp ')
        value = checkSanityofVariable(deviceType, 'bgp_keepalive_interval', bgpArg2)
        if (value == 'ok'):
            command = (command + bgpArg2)
        else:
            retVal = 'Error-191'
            return retVal
        if (bgpArg3 is not None):
            value = checkSanityofVariable(deviceType, 'bgp_holdtime', bgpArg3)
            if (value == 'ok'):
                command = ((command + ' ') + bgpArg3)
            else:
                retVal = 'Error-192'
                return retVal
        else:
            retVal = 'Error-192'
            return retVal
    elif (bgpArg1 == 'vrf'):
        command = ((command + bgpArg1) + ' default')
    else:
        retVal = 'Error-192'
        return retVal
    command = (command + '\n')
    retVal = (retVal + waitForDeviceResponse(command, prompt, timeout, obj))
    command = 'exit \n'
    retVal = (retVal + waitForDeviceResponse(command, '(config)#', timeout, obj))
    return retVal