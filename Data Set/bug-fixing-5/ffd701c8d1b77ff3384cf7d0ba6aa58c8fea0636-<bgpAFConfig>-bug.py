def bgpAFConfig(obj, deviceType, prompt, timeout, bgpAFArg1, bgpAFArg2, bgpAFArg3, bgpAFArg4, bgpAFArg5, bgpAFArg6):
    retVal = ''
    command = ''
    timeout = timeout
    if (bgpAFArg1 == 'aggregate-address'):
        command = ((command + bgpAFArg1) + ' ')
        value = checkSanityofVariable(deviceType, 'bgp_aggregate_prefix', bgpAFArg2)
        if (value == 'ok'):
            command = ((command + bgpAFArg2) + ' ')
            if (bgpAFArg2 is None):
                command = command
            elif ((bgpAFArg2 == 'as-set') or (bgpAFArg2 == 'summary-only')):
                command = ((command + bgpAFArg2) + ' ')
                if (bgpAFArg3 is None):
                    command = command
                elif (bgpAFArg2 == 'as-set'):
                    command = (command + 'summary-only')
                else:
                    command = (command + 'as-set')
            else:
                retVal = 'Error-297'
                return retVal
        else:
            retVal = 'Error-296'
            return retVal
    elif (bgpAFArg1 == 'client-to-client'):
        command = ((command + bgpAFArg1) + ' reflection ')
    elif (bgpAFArg1 == 'dampening'):
        command = ((command + bgpAFArg1) + ' ')
        if (bgpAFArg2 == 'route-map'):
            command = ((command + bgpAFArg2) + ' ')
            value = checkSanityofVariable(deviceType, 'addrfamily_routemap_name', bgpAFArg3)
            if (value == 'ok'):
                command = (command + bgpAFArg3)
            else:
                retVal = 'Error-196'
                return retVal
        elif (bgpAFArg2 is not None):
            value = checkSanityofVariable(deviceType, 'reachability_half_life', bgpAFArg2)
            if (value == 'ok'):
                command = ((command + bgpAFArg2) + ' ')
                if (bgpAFArg3 is not None):
                    value1 = checkSanityofVariable(deviceType, 'start_reuse_route_value', bgpAFArg3)
                    value2 = checkSanityofVariable(deviceType, 'start_suppress_route_value', bgpAFArg4)
                    value3 = checkSanityofVariable(deviceType, 'max_duration_to_suppress_route', bgpAFArg5)
                    if ((value1 == 'ok') and (value2 == 'ok') and (value3 == 'ok')):
                        command = ((((((command + bgpAFArg3) + ' ') + bgpAFArg4) + ' ') + bgpAFArg5) + ' ')
                        if (bgpAFArg6 is not None):
                            value = checkSanityofVariable(deviceType, 'unreachability_halftime_for_penalty', bgpAFArg6)
                            if (value == 'ok'):
                                command = (command + bgpAFArg6)
                    else:
                        retVal = 'Error-295'
                        return retVal
                else:
                    command = command
            else:
                retVal = 'Error-294'
                return retVal
    elif (bgpAFArg1 == 'distance'):
        command = ((command + bgpAFArg1) + ' ')
        value = checkSanityofVariable(deviceType, 'distance_external_AS', bgpAFArg2)
        if (value == 'ok'):
            command = ((command + bgpAFArg2) + ' ')
            value = checkSanityofVariable(deviceType, 'distance_internal_AS', bgpAFArg3)
            if (value == 'ok'):
                command = ((command + bgpAFArg3) + ' ')
                value = checkSanityofVariable(deviceType, 'distance_local_routes', bgpAFArg4)
                if (value == 'ok'):
                    command = (command + bgpAFArg4)
                else:
                    retVal = 'Error-291'
                    return retVal
            else:
                retVal = 'Error-292'
                return retVal
        else:
            retVal = 'Error-293'
            return retVal
    elif (bgpAFArg1 == 'maximum-paths'):
        command = ((command + bgpAFArg1) + ' ')
        value = checkSanityofVariable(deviceType, 'maxpath_option', bgpAFArg2)
        if (value == 'ok'):
            command = ((command + bgpAFArg2) + ' ')
            value = checkSanityofVariable(deviceType, 'maxpath_numbers', bgpAFArg3)
            if (value == 'ok'):
                command = (command + bgpAFArg3)
            else:
                retVal = 'Error-199'
                return retVal
        else:
            retVal = 'Error-290'
            return retVal
    elif (bgpAFArg1 == 'network'):
        command = ((command + bgpAFArg1) + ' ')
        if (bgpAFArg2 == 'synchronization'):
            command = (command + bgpAFArg2)
        else:
            value = checkSanityofVariable(deviceType, 'network_ip_prefix_with_mask', bgpAFArg2)
            if (value == 'ok'):
                command = ((command + bgpAFArg2) + ' ')
                if ((bgpAFArg3 is not None) and (bgpAFArg3 == 'backdoor')):
                    command = (command + bgpAFArg3)
                elif ((bgpAFArg3 is not None) and (bgpAFArg3 == 'route-map')):
                    command = (command + bgpAFArg3)
                    value = checkSanityofVariable(deviceType, 'addrfamily_routemap_name', bgpAFArg4)
                    if (value == 'ok'):
                        command = ((command + bgpAFArg4) + ' ')
                        if ((bgpAFArg5 is not None) and (bgpAFArg5 == 'backdoor')):
                            command = (command + bgpAFArg5)
                        else:
                            retVal = 'Error-298'
                            return retVal
                    else:
                        retVal = 'Error-196'
                        return retVal
                else:
                    command = command
            else:
                value = checkSanityofVariable(deviceType, 'network_ip_prefix_value', bgpAFArg2)
                if (value == 'ok'):
                    command = ((command + bgpAFArg2) + ' ')
                    if ((bgpAFArg3 is not None) and (bgpAFArg3 == 'backdoor')):
                        command = (command + bgpAFArg3)
                    elif ((bgpAFArg3 is not None) and (bgpAFArg3 == 'route-map')):
                        command = (command + bgpAFArg3)
                        value = checkSanityofVariable(deviceType, 'addrfamily_routemap_name', bgpAFArg4)
                        if (value == 'ok'):
                            command = ((command + bgpAFArg4) + ' ')
                            if ((bgpAFArg5 is not None) and (bgpAFArg5 == 'backdoor')):
                                command = (command + bgpAFArg5)
                            else:
                                retVal = 'Error-298'
                                return retVal
                        else:
                            retVal = 'Error-196'
                            return retVal
                    elif ((bgpAFArg3 is not None) and (bgpAFArg3 == 'mask')):
                        command = (command + bgpAFArg3)
                        value = checkSanityofVariable(deviceType, 'network_ip_prefix_mask', bgpAFArg4)
                        if (value == 'ok'):
                            command = ((command + bgpAFArg4) + ' ')
                        else:
                            retVal = 'Error-299'
                            return retVal
                    else:
                        command = command
                else:
                    retVal = 'Error-300'
                    return retVal
    elif (bgpAFArg1 == 'nexthop'):
        command = ((command + bgpAFArg1) + ' trigger-delay critical ')
        value = checkSanityofVariable(deviceType, 'nexthop_crtitical_delay', bgpAFArg2)
        if (value == 'ok'):
            command = ((command + bgpAFArg2) + ' ')
            value = checkSanityofVariable(deviceType, 'nexthop_noncrtitical_delay', bgpAFArg3)
            if (value == 'ok'):
                command = ((command + bgpAFArg3) + ' ')
            else:
                retVal = 'Error-198'
                return retVal
        else:
            retVal = 'Error-197'
            return retVal
    elif (bgpAFArg1 == 'redistribute'):
        command = ((command + bgpAFArg1) + ' ')
        value = checkSanityofVariable(deviceType, 'addrfamily_redistribute_option', bgpAFArg2)
        if (value == 'ok'):
            command = ((command + bgpAFArg2) + ' ')
            if (bgpAFArg2 is not None):
                command = (command + 'route-map ')
                value = checkSanityofVariable(deviceType, 'addrfamily_routemap_name', bgpAFArg3)
                if (value == 'ok'):
                    command = (command + bgpAFArg3)
                else:
                    retVal = 'Error-196'
                    return retVal
        else:
            retVal = 'Error-195'
            return retVal
    elif ((bgpAFArg1 == 'save') or (bgpAFArg1 == 'synchronization')):
        command = (command + bgpAFArg1)
    else:
        retVal = 'Error-194'
        return retVal
    command = (command + '\n')
    retVal = (retVal + waitForDeviceResponse(command, prompt, timeout, obj))
    command = 'exit \n'
    retVal = (retVal + waitForDeviceResponse(command, '(config-router)#', timeout, obj))
    return retVal