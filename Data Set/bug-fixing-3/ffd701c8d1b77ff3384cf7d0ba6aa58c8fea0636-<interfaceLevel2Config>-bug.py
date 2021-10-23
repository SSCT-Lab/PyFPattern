def interfaceLevel2Config(obj, deviceType, prompt, timeout, interfaceL2Arg1, interfaceL2Arg2, interfaceL2Arg3, interfaceL2Arg4, interfaceL2Arg5, interfaceL2Arg6, interfaceL2Arg7):
    retVal = ''
    command = ''
    if (interfaceL2Arg1 == 'aggregation-group'):
        command = (interfaceL2Arg1 + ' ')
        value = checkSanityofVariable(deviceType, 'aggregation_group_no', interfaceL2Arg2)
        if (value == 'ok'):
            command = ((command + interfaceL2Arg2) + ' mode ')
            value = checkSanityofVariable(deviceType, 'aggregation_group_mode', interfaceL2Arg3)
            if (value == 'ok'):
                command = (command + interfaceL2Arg3)
            else:
                retVal = 'Error-200'
                return retVal
        else:
            retVal = 'Error-201'
            return retVal
    elif (interfaceL2Arg1 == 'bfd'):
        command = (interfaceL2Arg1 + ' ')
        value = checkSanityofVariable(deviceType, 'bfd_options', interfaceL2Arg2)
        if (value == 'ok'):
            if (interfaceL2Arg2 == 'echo'):
                command = (command + interfaceL2Arg2)
            elif (interfaceL2Arg2 == 'interval'):
                command = ((command + interfaceL2Arg2) + ' ')
                value = checkSanityofVariable(deviceType, 'bfd_interval', interfaceL2Arg3)
                if (value == 'ok'):
                    command = (command + interfaceL2Arg3)
                    value = checkSanityofVariable(deviceType, 'bfd_minrx', interfaceL2Arg4)
                    if (value == 'ok'):
                        command = ((command + ' minrx ') + interfaceL2Arg4)
                        value = checkSanityofVariable(deviceType, 'bfd_ multiplier', interfaceL2Arg5)
                        if (value == 'ok'):
                            command = ((command + ' multiplier ') + interfaceL2Arg5)
                        else:
                            retVal = 'Error-236'
                            return retVal
                    else:
                        retVal = 'Error-235'
                        return retVal
                else:
                    retVal = 'Error-234'
                    return retVal
            elif (interfaceL2Arg2 == 'authentication'):
                command = ((command + interfaceL2Arg2) + ' ')
                value = checkSanityofVariable(deviceType, 'bfd_auth_options', interfaceL2Arg3)
                if (value == 'ok'):
                    command = ((command + interfaceL2Arg3) + ' ')
                    if ((interfaceL2Arg3 == 'keyed-md5') or (interfaceL2Arg3 == 'keyed-sha1') or (interfaceL2Arg3 == 'meticulous-keyed-md5') or (interfaceL2Arg3 == 'meticulous-keyed-sha1') or (interfaceL2Arg3 == 'simple')):
                        value = checkSanityofVariable(deviceType, 'bfd_key_options', interfaceL2Arg4)
                        if (value == 'ok'):
                            command = ((command + interfaceL2Arg4) + ' ')
                            if (interfaceL2Arg4 == 'key-chain'):
                                value = checkSanityofVariable(deviceType, 'bfd_key_chain', interfaceL2Arg5)
                                if (value == 'ok'):
                                    command = (command + interfaceL2Arg5)
                                else:
                                    retVal = 'Error-237'
                                    return retVal
                            elif (interfaceL2Arg4 == 'key-id'):
                                value = checkSanityofVariable(deviceType, 'bfd_key_id', interfaceL2Arg5)
                                if (value == 'ok'):
                                    command = (command + interfaceL2Arg5)
                                    command = (command + ' key ')
                                    value = checkSanityofVariable(deviceType, 'bfd_key_name', interfaceL2Arg6)
                                    if (value == 'ok'):
                                        command = (command + interfaceL2Arg6)
                                    else:
                                        retVal = 'Error-238'
                                        return retVal
                                else:
                                    retVal = 'Error-239'
                                    return retVal
                        else:
                            retVal = 'Error-240'
                            return retVal
                else:
                    retVal = 'Error-241'
                    return retVal
            elif ((interfaceL2Arg2 == 'ipv4') or (interfaceL2Arg2 == 'ipv6')):
                command = ((command + interfaceL2Arg2) + ' ')
                value = checkSanityofVariable(deviceType, 'bfd_ipv4_options', interfaceL2Arg3)
                if (value == 'ok'):
                    command = ((command + interfaceL2Arg3) + ' ')
                    if (interfaceL2Arg3 == 'authentication'):
                        value = checkSanityofVariable(deviceType, 'bfd_auth_options', interfaceL2Arg4)
                        if (value == 'ok'):
                            command = ((command + interfaceL2Arg4) + ' ')
                            if ((interfaceL2Arg4 == 'keyed-md5') or (interfaceL2Arg4 == 'keyed-sha1') or (interfaceL2Arg4 == 'meticulous-keyed-md5') or (interfaceL2Arg4 == 'meticulous-keyed-sha1') or (interfaceL2Arg4 == 'simple')):
                                value = checkSanityofVariable(deviceType, 'bfd_key_options', interfaceL2Arg5)
                                if (value == 'ok'):
                                    command = ((command + interfaceL2Arg5) + ' ')
                                    if (interfaceL2Arg5 == 'key-chain'):
                                        value = checkSanityofVariable(deviceType, 'bfd_key_chain', interfaceL2Arg6)
                                        if (value == 'ok'):
                                            command = (command + interfaceL2Arg6)
                                        else:
                                            retVal = 'Error-237'
                                            return retVal
                                    elif (interfaceL2Arg5 == 'key-id'):
                                        value = checkSanityofVariable(deviceType, 'bfd_key_id', interfaceL2Arg6)
                                        if (value == 'ok'):
                                            command = ((command + interfaceL2Arg6) + ' key ')
                                            value = checkSanityofVariable(deviceType, 'bfd_key_name', interfaceL2Arg7)
                                            if (value == 'ok'):
                                                command = (command + interfaceL2Arg7)
                                            else:
                                                retVal = 'Error-238'
                                                return retVal
                                        else:
                                            retVal = 'Error-239'
                                            return retVal
                                    else:
                                        retVal = 'Error-240'
                                        return retVal
                                else:
                                    retVal = 'Error-240'
                                    return retVal
                        else:
                            retVal = 'Error-241'
                            return retVal
                    elif (interfaceL2Arg3 == 'echo'):
                        command = (command + interfaceL2Arg3)
                    elif (interfaceL2Arg3 == 'interval'):
                        command = ((command + interfaceL2Arg3) + ' ')
                        value = checkSanityofVariable(deviceType, 'bfd_interval', interfaceL2Arg4)
                        if (value == 'ok'):
                            command = (command + interfaceL2Arg4)
                            value = checkSanityofVariable(deviceType, 'bfd_minrx', interfaceL2Arg5)
                            if (value == 'ok'):
                                command = ((command + ' minrx ') + interfaceL2Arg5)
                                value = checkSanityofVariable(deviceType, 'bfd_ multiplier', interfaceL2Arg6)
                                if (value == 'ok'):
                                    command = ((command + ' multiplier ') + interfaceL2Arg6)
                                else:
                                    retVal = 'Error-236'
                                    return retVal
                            else:
                                retVal = 'Error-235'
                                return retVal
                        else:
                            retVal = 'Error-234'
                            return retVal
                else:
                    command = command
            elif (interfaceL2Arg2 == 'neighbor'):
                command = ((command + interfaceL2Arg2) + ' src-ip ')
                value = checkSanityofVariable(deviceType, 'bfd_neighbor_ip', interfaceL2Arg3)
                if (value == 'ok'):
                    command = ((command + interfaceL2Arg3) + ' dest-ip ')
                    value = checkSanityofVariable(deviceType, 'bfd_neighbor_ip', interfaceL2Arg4)
                    if (value == 'ok'):
                        command = ((command + interfaceL2Arg4) + ' ')
                        if (interfaceL2Arg5 is not None):
                            value = checkSanityofVariable(deviceType, 'bfd_neighbor_options', interfaceL2Arg5)
                            if (value == 'ok'):
                                command = ((command + interfaceL2Arg5) + ' ')
                                if (interfaceL2Arg6 is not None):
                                    if ((interfaceL2Arg6 == 'admin-down') or (interfaceL2Arg6 == 'non-persistent')):
                                        command = ((command + interfaceL2Arg6) + ' ')
                                        if ((interfaceL2Arg7 is not None) and (interfaceL2Arg7 == 'admin-down')):
                                            command = (command + interfaceL2Arg7)
                                        else:
                                            retVal = 'Error-277'
                                            return retVal
                                    else:
                                        retVal = 'Error-277'
                                        return retVal
                    else:
                        retVal = 'Error-242'
                        return retVal
                else:
                    retVal = 'Error-243'
                    return retVal
            else:
                retVal = 'Error-205'
                return retVal
        else:
            retVal = 'Error-205'
            return retVal
    elif (interfaceL2Arg1 == 'bridge-port'):
        command = (interfaceL2Arg1 + ' ')
        if (interfaceL2Arg2 is None):
            command = command
        elif (interfaceL2Arg2 == 'access'):
            command = ((command + interfaceL2Arg2) + ' vlan ')
            value = checkSanityofVariable(deviceType, 'bfd_access_vlan', interfaceL2Arg3)
            if (value == 'ok'):
                command = (command + interfaceL2Arg3)
            else:
                retVal = 'Error-202'
                return retVal
        elif (interfaceL2Arg2 == 'mode'):
            command = ((command + interfaceL2Arg2) + ' ')
            value = checkSanityofVariable(deviceType, 'bfd_bridgeport_mode', interfaceL2Arg3)
            if (value == 'ok'):
                command = (command + interfaceL2Arg3)
            else:
                retVal = 'Error-203'
                return retVal
        elif (interfaceL2Arg2 == 'trunk'):
            command = ((command + interfaceL2Arg2) + ' ')
            value = checkSanityofVariable(deviceType, 'trunk_options', interfaceL2Arg3)
            if (value == 'ok'):
                command = ((command + interfaceL2Arg3) + ' ')
                if ((interfaceL2Arg3 == 'allowed') or (interfaceL2Arg3 == 'native')):
                    command = (command + 'vlan ')
                    if ((interfaceL2Arg4 == 'all') or (interfaceL2Arg4 == 'none')):
                        command = (command + interfaceL2Arg4)
                    elif ((interfaceL2Arg4 == 'add') or (interfaceL2Arg4 == 'remove') or (interfaceL2Arg4 == 'none')):
                        command = ((command + interfaceL2Arg4) + ' ')
                        value = checkSanityofVariable(deviceType, 'bfd_access_vlan', interfaceL2Arg5)
                        if (value == 'ok'):
                            command = (command + interfaceL2Arg5)
                        else:
                            retVal = 'Error-202'
                            return retVal
                    else:
                        value = checkSanityofVariable(deviceType, 'bfd_access_vlan', interfaceL2Arg4)
                        if (value == 'ok'):
                            command = (command + interfaceL2Arg4)
                        else:
                            retVal = 'Error-202'
                            return retVal
                else:
                    retVal = 'Error-204'
                    return retVal
            else:
                retVal = 'Error-204'
                return retVal
        else:
            retVal = 'Error-205'
            return retVal
    elif (interfaceL2Arg1 == 'description'):
        command = (interfaceL2Arg1 + ' ')
        value = checkSanityofVariable(deviceType, 'portCh_description', interfaceL2Arg2)
        if (value == 'ok'):
            command = (command + interfaceL2Arg2)
        else:
            retVal = 'Error-206'
            return retVal
    elif (interfaceL2Arg1 == 'duplex'):
        command = (interfaceL2Arg1 + ' ')
        value = checkSanityofVariable(deviceType, 'duplex_option', interfaceL2Arg2)
        if (value == 'ok'):
            command = (command + interfaceL2Arg2)
        else:
            retVal = 'Error-207'
            return retVal
    elif (interfaceL2Arg1 == 'flowcontrol'):
        command = (interfaceL2Arg1 + ' ')
        value = checkSanityofVariable(deviceType, 'flowcontrol_options', interfaceL2Arg2)
        if (value == 'ok'):
            command = ((command + interfaceL2Arg2) + ' ')
            if ((interfaceL2Arg3 == 'on') or (interfaceL2Arg3 == 'off')):
                command = (command + interfaceL2Arg3)
            else:
                retVal = 'Error-208'
                return retVal
        else:
            retVal = 'Error-209'
            return retVal
    elif (interfaceL2Arg1 == 'ip'):
        command = (interfaceL2Arg1 + ' ')
        value = checkSanityofVariable(deviceType, 'portchannel_ip_options', interfaceL2Arg2)
        if (value == 'ok'):
            command = ((command + interfaceL2Arg2) + ' ')
            if (interfaceL2Arg2 == 'access-group'):
                value = checkSanityofVariable(deviceType, 'accessgroup_name', interfaceL2Arg3)
                if (value == 'ok'):
                    command = ((command + interfaceL2Arg3) + ' ')
                    if ((interfaceL2Arg4 == 'in') or (interfaceL2Arg4 == 'out')):
                        command = (command + interfaceL2Arg4)
                    else:
                        retVal = 'Error-245'
                        return retVal
                else:
                    retVal = 'Error-246'
                    return retVal
            elif (interfaceL2Arg2 == 'address'):
                if (interfaceL2Arg3 == 'dhcp'):
                    command = (command + interfaceL2Arg3)
                elif (interfaceL2Arg3 is not None):
                    value = checkSanityofVariable(deviceType, 'portchannel_ipv4', interfaceL2Arg3)
                    if (value == 'ok'):
                        command = ((command + interfaceL2Arg3) + ' ')
                        value = checkSanityofVariable(deviceType, 'portchannel_ipv4', interfaceL2Arg4)
                        if (value == 'ok'):
                            command = ((command + interfaceL2Arg4) + ' ')
                            if (interfaceL2Arg5 == 'secondary'):
                                command = (command + interfaceL2Arg5)
                            elif (interfaceL2Arg5 is None):
                                command = (command + interfaceL2Arg5)
                            else:
                                retVal = 'Error-278'
                                return retVal
                        else:
                            retVal = 'Error-279'
                            return retVal
                    else:
                        value = checkSanityofVariable(deviceType, 'portchannel_ipv4_mask', interfaceL2Arg3)
                        if (value == 'ok'):
                            command = ((command + interfaceL2Arg3) + ' ')
                            if (interfaceL2Arg4 == 'secondary'):
                                command = (command + interfaceL2Arg4)
                            elif (interfaceL2Arg4 is None):
                                command = (command + interfaceL2Arg4)
                            else:
                                retVal = 'Error-278'
                                return retVal
                        else:
                            retVal = 'Error-279'
                            return retVal
            elif (interfaceL2Arg2 == 'arp'):
                value = checkSanityofVariable(deviceType, 'arp_ipaddress', interfaceL2Arg3)
                if (value == 'ok'):
                    command = ((command + interfaceL2Arg3) + ' ')
                    value = checkSanityofVariable(deviceType, 'arp_macaddress', interfaceL2Arg4)
                    if (value == 'ok'):
                        command = ((command + interfaceL2Arg4) + ' ')
                    else:
                        retVal = 'Error-247'
                        return retVal
                elif (interfaceL2Arg3 == 'timeout'):
                    command = ((command + interfaceL2Arg3) + ' ')
                    value = checkSanityofVariable(deviceType, 'arp_timeout_value', interfaceL2Arg4)
                    if (value == 'ok'):
                        command = ((command + interfaceL2Arg4) + ' ')
                    else:
                        retVal = 'Error-248'
                        return retVal
                else:
                    retVal = 'Error-249'
                    return retVal
            elif (interfaceL2Arg2 == 'dhcp'):
                if (interfaceL2Arg3 == 'client'):
                    command = ((command + interfaceL2Arg3) + ' ')
                    if (interfaceL2Arg4 == 'class-id'):
                        command = ((command + interfaceL2Arg3) + ' ')
                        if (interfaceL2Arg4 is not None):
                            command = (command + interfaceL2Arg4)
                    elif (interfaceL2Arg4 == 'request'):
                        command = ((command + interfaceL2Arg4) + ' ')
                        if ((interfaceL2Arg5 == 'bootfile-name') or (interfaceL2Arg5 == 'host-name') or (interfaceL2Arg5 == 'log-server') or (interfaceL2Arg5 == 'tftp-server-name')):
                            command = ((command + interfaceL2Arg5) + ' ')
                        else:
                            retVal = 'Error-250'
                            return retVal
                    else:
                        retVal = 'Error-251'
                        return retVal
                elif (interfaceL2Arg3 == 'relay'):
                    command = ((command + interfaceL2Arg3) + ' address ')
                    value = checkSanityofVariable(deviceType, 'relay_ipaddress', interfaceL2Arg4)
                    if (value == 'ok'):
                        command = (command + interfaceL2Arg4)
                    else:
                        retVal = 'Error-252'
                        return retVal
                else:
                    retVal = 'Error-253'
                    return retVal
            elif (interfaceL2Arg2 == 'ospf'):
                value = checkSanityofVariable(deviceType, 'ip_ospf_options', interfaceL2Arg3)
                if (value == 'ok'):
                    retVal = 'Error-102'
                    return retVal
                else:
                    retVal = 'Error-254'
                    return retVal
            elif (interfaceL2Arg2 == 'port'):
                command = (command + 'access-group ')
                value = checkSanityofVariable(deviceType, 'accessgroup_name', interfaceL2Arg3)
                if (value == 'ok'):
                    command = ((command + interfaceL2Arg3) + ' in')
                else:
                    retVal = 'Error-246'
                    return retVal
            elif (interfaceL2Arg2 == 'port-unreachable'):
                command = (command + interfaceL2Arg2)
            elif (interfaceL2Arg2 == 'redirects'):
                command = (command + interfaceL2Arg2)
            elif (interfaceL2Arg2 == 'router'):
                command = ((command + interfaceL2Arg2) + ' 0 ')
                if ((interfaceL2Arg3 == 'area') or (interfaceL2Arg3 == 'multi-area')):
                    command = (command + interfaceL2Arg3)
                    value = checkSanityofVariable(deviceType, 'ospf_id_decimal_value', interfaceL2Arg4)
                    if (value == 'ok'):
                        command = (command + interfaceL2Arg4)
                    else:
                        value = checkSanityofVariable(deviceType, 'ospf_id_ipaddres_value', interfaceL2Arg4)
                        if (value == 'ok'):
                            command = (command + interfaceL2Arg4)
                        else:
                            retVal = 'Error-255'
                            return retVal
                else:
                    retVal = 'Error-256'
                    return retVal
            elif (interfaceL2Arg2 == 'unreachables'):
                command = (command + interfaceL2Arg2)
            else:
                retVal = 'Error-244'
                return retVal
        else:
            retVal = 'Error-244'
            return retVal
    elif (interfaceL2Arg1 == 'ipv6'):
        command = (interfaceL2Arg1 + ' ')
        value = checkSanityofVariable(deviceType, 'portchannel_ipv6_options', interfaceL2Arg2)
        if (value == 'ok'):
            command = ((command + interfaceL2Arg2) + ' ')
            if (interfaceL2Arg2 == 'address'):
                if (interfaceL2Arg3 == 'dhcp'):
                    command = (command + interfaceL2Arg3)
                else:
                    value = checkSanityofVariable(deviceType, 'portchannel_ipv6_address', interfaceL2Arg3)
                    if (value == 'ok'):
                        command = ((command + interfaceL2Arg3) + ' ')
                        if ((interfaceL2Arg4 == 'anycast') or (interfaceL2Arg4 == 'secondary') or (interfaceL2Arg4 is None)):
                            command = (command + interfaceL2Arg4)
                        else:
                            retVal = 'Error-276'
                            return retVal
                    else:
                        retVal = 'Error-275'
                        return retVal
            elif (interfaceL2Arg2 == 'dhcp'):
                value = checkSanityofVariable(deviceType, 'portchannel_ipv6_dhcp', interfaceL2Arg3)
                if (value == 'ok'):
                    command = ((command + 'relay address ') + interfaceL2Arg3)
                    if (interfaceL2Arg4 is not None):
                        if (interfaceL2Arg4 == 'ethernet'):
                            value = checkSanityofVariable(deviceType, 'portchannel_ipv6_dhcp_ethernet', interfaceL2Arg4)
                            if (value == 'ok'):
                                command = ((command + ' interface ethernet ') + interfaceL2Arg4)
                            else:
                                retVal = 'Error-271'
                                return retVal
                        elif (interfaceL2Arg4 == 'vlan'):
                            value = checkSanityofVariable(deviceType, 'portchannel_ipv6_dhcp_vlan', interfaceL2Arg4)
                            if (value == 'ok'):
                                command = ((command + ' interface vlan ') + interfaceL2Arg4)
                            else:
                                retVal = 'Error-272'
                                return retVal
                        else:
                            retVal = 'Error-270'
                            return retVal
                else:
                    retVal = 'Error-269'
                    return retVal
            elif (interfaceL2Arg2 == 'link-local'):
                value = checkSanityofVariable(deviceType, 'portchannel_ipv6_linklocal', interfaceL2Arg3)
                if (value == 'ok'):
                    command = (command + interfaceL2Arg3)
                else:
                    retVal = 'Error-273'
                    return retVal
            elif (interfaceL2Arg2 == 'nd'):
                retVal = 'Error-102'
                return retVal
            elif (interfaceL2Arg2 == 'neighbor'):
                value = checkSanityofVariable(deviceType, 'portchannel_ipv6_neighbor_address', interfaceL2Arg3)
                if (value == 'ok'):
                    command = ((command + interfaceL2Arg3) + ' ')
                    value = checkSanityofVariable(deviceType, 'portchannel_ipv6_neighbor_mac', interfaceL2Arg4)
                    if (value == 'ok'):
                        command = (command + interfaceL2Arg4)
                    else:
                        retVal = 'Error-267'
                        return retVal
                else:
                    retVal = 'Error-268'
                    return retVal
            else:
                retVal = 'Error-266'
                return retVal
        else:
            retVal = 'Error-102'
            return retVal
    elif (interfaceL2Arg1 == 'lacp'):
        command = (interfaceL2Arg1 + ' ')
        value = checkSanityofVariable(deviceType, 'lacp_options', interfaceL2Arg2)
        if (value == 'ok'):
            command = ((command + interfaceL2Arg2) + ' ')
            if (interfaceL2Arg2 == 'port-priority'):
                value = checkSanityofVariable(deviceType, 'port_priority', interfaceL2Arg3)
                if (value == 'ok'):
                    command = (command + interfaceL2Arg3)
                else:
                    retVal = 'Error-210'
                    return retVal
            elif (interfaceL2Arg2 == 'suspend-individual'):
                command = (command + interfaceL2Arg3)
            elif (interfaceL2Arg2 == 'timeout'):
                command = ((command + interfaceL2Arg2) + ' ')
                if ((interfaceL2Arg3 == 'long') or (interfaceL2Arg3 == 'short')):
                    command = (command + interfaceL2Arg3)
                else:
                    retVal = 'Error-211'
                    return retVal
            else:
                retVal = 'Error-212'
                return retVal
        else:
            retVal = 'Error-212'
            return retVal
    elif (interfaceL2Arg1 == 'lldp'):
        command = (interfaceL2Arg1 + ' ')
        value = checkSanityofVariable(deviceType, 'lldp_options', interfaceL2Arg2)
        if (value == 'ok'):
            command = ((command + interfaceL2Arg2) + ' ')
            if ((interfaceL2Arg2 == 'receive') or (interfaceL2Arg2 == 'trap-notification') or (interfaceL2Arg2 == 'transmit')):
                command = command
            elif (interfaceL2Arg2 == 'tlv-select'):
                value = checkSanityofVariable(deviceType, 'lldp_tlv_options', interfaceL2Arg3)
                if (value == 'ok'):
                    command = (command + interfaceL2Arg3)
                else:
                    retVal = 'Error-213'
                    return retVal
            else:
                retVal = 'Error-214'
                return retVal
        else:
            retVal = 'Error-214'
            return retVal
    elif (interfaceL2Arg1 == 'load-interval'):
        command = (interfaceL2Arg1 + ' ')
        value = checkSanityofVariable(deviceType, 'load_interval_delay', interfaceL2Arg2)
        if (value == 'ok'):
            command = (command + interfaceL2Arg2)
        elif (interfaceL2Arg2 == 'counter'):
            command = ((command + interfaceL2Arg2) + ' ')
            value = checkSanityofVariable(deviceType, 'load_interval_counter', interfaceL2Arg3)
            if (value == 'ok'):
                command = ((command + interfaceL2Arg3) + ' ')
                value = checkSanityofVariable(deviceType, 'load_interval_delay', interfaceL2Arg4)
                if (value == 'ok'):
                    command = (command + interfaceL2Arg4)
                else:
                    retVal = 'Error-215'
                    return retVal
            else:
                retVal = 'Error-216'
                return retVal
        else:
            retVal = 'Error-217'
            return retVal
    elif (interfaceL2Arg1 == 'mac'):
        command = (interfaceL2Arg1 + ' port access-group ')
        value = checkSanityofVariable(deviceType, 'mac_accessgroup_name', interfaceL2Arg2)
        if (value == 'ok'):
            command = (command + interfaceL2Arg2)
        else:
            retVal = 'Error-218'
            return retVal
    elif (interfaceL2Arg1 == 'mac-address'):
        command = (interfaceL2Arg1 + ' ')
        value = checkSanityofVariable(deviceType, 'mac_address', interfaceL2Arg2)
        if (value == 'ok'):
            command = (command + interfaceL2Arg2)
        else:
            retVal = 'Error-219'
            return retVal
    elif (interfaceL2Arg1 == 'mac-learn'):
        command = (interfaceL2Arg1 + ' disable')
    elif (interfaceL2Arg1 == 'microburst-detection'):
        command = (interfaceL2Arg1 + ' enable threshold ')
        value = checkSanityofVariable(deviceType, 'microburst_threshold', interfaceL2Arg2)
        if (value == 'ok'):
            command = (command + interfaceL2Arg2)
        else:
            retVal = 'Error-220'
            return retVal
    elif (interfaceL2Arg1 == 'mtu'):
        command = (interfaceL2Arg1 + ' ')
        value = checkSanityofVariable(deviceType, 'mtu_value', interfaceL2Arg2)
        if (value == 'ok'):
            command = (command + interfaceL2Arg2)
        else:
            retVal = 'Error-221'
            return retVal
    elif (interfaceL2Arg1 == 'service'):
        command = (interfaceL2Arg1 + ' instance ')
        value = checkSanityofVariable(deviceType, 'service_instance', interfaceL2Arg2)
        if (value == 'ok'):
            command = (command + interfaceL2Arg2)
        else:
            retVal = 'Error-222'
            return retVal
    elif (interfaceL2Arg1 == 'service-policy'):
        command = (interfaceL2Arg1 + ' ')
        value = checkSanityofVariable(deviceType, 'service_policy_options', interfaceL2Arg2)
        if (value == 'ok'):
            command = ((command + interfaceL2Arg2) + ' ')
            if ((interfaceL2Arg2 == 'input') or (interfaceL2Arg2 == 'output')):
                value = checkSanityofVariable(deviceType, 'service_policy_name', interfaceL2Arg3)
                if (value == 'ok'):
                    command = (command + interfaceL2Arg3)
                else:
                    retVal = 'Error-223'
                    return retVal
            elif (interfaceL2Arg2 == 'copp-system-policy'):
                command = (command + 'class all')
            elif ((interfaceL2Arg2 == 'type') and (interfaceL2Arg3 == 'qos')):
                command = ((command + interfaceL2Arg3) + ' ')
                if ((interfaceL2Arg4 == 'input') or (interfaceL2Arg4 == 'output')):
                    value = checkSanityofVariable(deviceType, 'service_policy_name', interfaceL2Arg5)
                    if (value == 'ok'):
                        command = (command + interfaceL2Arg5)
                else:
                    retVal = 'Error-223'
                    return retVal
            elif ((interfaceL2Arg2 == 'type') and (interfaceL2Arg3 == 'queuing')):
                command = ((command + interfaceL2Arg3) + ' ')
                if ((interfaceL2Arg4 == 'input') or (interfaceL2Arg4 == 'output')):
                    value = checkSanityofVariable(deviceType, 'service_policy_name', interfaceL2Arg5)
                    if (value == 'ok'):
                        command = (command + interfaceL2Arg5)
                else:
                    retVal = 'Error-223'
                    return retVal
            else:
                retVal = 'Error-224'
                return retVal
    elif (interfaceL2Arg1 == 'shutdown'):
        command = interfaceL2Arg1
    elif (interfaceL2Arg1 == 'no shutdown'):
        command = interfaceL2Arg1
    elif (interfaceL2Arg1 == 'snmp'):
        command = (interfaceL2Arg1 + '  trap link-status ')
    elif (interfaceL2Arg1 == 'spanning-tree'):
        command = (interfaceL2Arg1 + ' ')
        value = checkSanityofVariable(deviceType, 'spanning_tree_options', interfaceL2Arg2)
        if (value == 'ok'):
            if (interfaceL2Arg2 == 'bpdufilter'):
                command = ((command + interfaceL2Arg2) + ' ')
                if ((interfaceL2Arg3 == 'enable') or (interfaceL2Arg3 == 'disable')):
                    command = (command + interfaceL2Arg3)
                else:
                    retVal = 'Error-257'
                    return retVal
            elif (interfaceL2Arg2 == 'bpduguard'):
                command = ((command + interfaceL2Arg2) + ' ')
                if ((interfaceL2Arg3 == 'enable') or (interfaceL2Arg3 == 'disable')):
                    command = (command + interfaceL2Arg3)
                else:
                    retVal = 'Error-258'
                    return retVal
            elif (interfaceL2Arg2 == 'cost'):
                command = ((command + interfaceL2Arg2) + ' ')
                value = checkSanityofVariable(deviceType, 'spanning_tree_cost', interfaceL2Arg3)
                if (value == 'ok'):
                    command = (command + interfaceL2Arg3)
                elif (interfaceL2Arg3 == 'auto'):
                    command = (command + interfaceL2Arg3)
                else:
                    retVal = 'Error-259'
                    return retVal
            elif ((interfaceL2Arg2 == 'disable') or (interfaceL2Arg2 == 'enable')):
                command = ((command + interfaceL2Arg2) + ' ')
            elif (interfaceL2Arg2 == 'guard'):
                command = ((command + interfaceL2Arg2) + ' ')
                if ((interfaceL2Arg3 == 'loop') or (interfaceL2Arg3 == 'root')):
                    command = (command + interfaceL2Arg3)
                else:
                    retVal = 'Error-260'
                    return retVal
            elif (interfaceL2Arg2 == 'link-type'):
                command = ((command + interfaceL2Arg2) + ' ')
                if ((interfaceL2Arg3 == 'auto') or (interfaceL2Arg3 == 'point-to-point') or (interfaceL2Arg3 == 'shared')):
                    command = (command + interfaceL2Arg3)
                else:
                    retVal = 'Error-261'
                    return retVal
            elif (interfaceL2Arg2 == 'mst'):
                command = ((command + interfaceL2Arg2) + ' ')
                value = checkSanityofVariable(deviceType, 'spanning_tree_interfacerange', interfaceL2Arg3)
                if (value == 'ok'):
                    command = ((command + interfaceL2Arg3) + ' ')
                    if (interfaceL2Arg4 == 'cost'):
                        command = ((command + interfaceL2Arg4) + ' ')
                        value = checkSanityofVariable(deviceType, 'spanning_tree_cost', interfaceL2Arg5)
                        if (value == 'ok'):
                            command = (command + interfaceL2Arg5)
                        elif (interfaceL2Arg5 == 'auto'):
                            command = (command + interfaceL2Arg5)
                        else:
                            retVal = 'Error-259'
                            return retVal
                    elif (interfaceL2Arg4 == 'port-priority'):
                        command = ((command + interfaceL2Arg4) + ' ')
                        value = checkSanityofVariable(deviceType, 'spanning_tree_portpriority', interfaceL2Arg5)
                        if (value == 'ok'):
                            command = (command + interfaceL2Arg5)
                        else:
                            retVal = 'Error-259'
                            return retVal
                    else:
                        retVal = 'Error-259'
                        return retVal
                else:
                    retVal = 'Error-263'
                    return retVal
            elif (interfaceL2Arg2 == 'port'):
                command = ((command + interfaceL2Arg2) + ' type edge')
            elif (interfaceL2Arg2 == 'port-priority'):
                command = ((command + interfaceL2Arg2) + ' ')
                value = checkSanityofVariable(deviceType, 'spanning_tree_portpriority', interfaceL2Arg3)
                if (value == 'ok'):
                    command = (command + interfaceL2Arg3)
                else:
                    retVal = 'Error-264'
                    return retVal
            elif (interfaceL2Arg2 == 'vlan'):
                command = ((command + interfaceL2Arg2) + ' ')
                value = checkSanityofVariable(deviceType, 'vlan_id_range', interfaceL2Arg3)
                if (value == 'ok'):
                    command = (command + interfaceL2Arg3)
                    if (interfaceL2Arg4 == 'cost'):
                        command = ((command + interfaceL2Arg4) + ' ')
                        value = checkSanityofVariable(deviceType, 'spanning_tree_cost', interfaceL2Arg5)
                        if (value == 'ok'):
                            command = (command + interfaceL2Arg5)
                        elif (interfaceL2Arg5 == 'auto'):
                            command = (command + interfaceL2Arg5)
                        else:
                            retVal = 'Error-263'
                            return retVal
                    elif (interfaceL2Arg4 == 'port-priority'):
                        command = ((command + interfaceL2Arg4) + ' ')
                        value = checkSanityofVariable(deviceType, 'spanning_tree_portpriority', interfaceL2Arg5)
                        if (value == 'ok'):
                            command = (command + interfaceL2Arg5)
                        else:
                            retVal = 'Error-264'
                            return retVal
                    else:
                        retVal = 'Error-264'
                        return retVal
                else:
                    retVal = 'Error-134'
                    return retVal
            else:
                retVal = 'Error-263'
                return retVal
    elif (interfaceL2Arg1 == 'speed'):
        command = (interfaceL2Arg1 + ' ')
        value = checkSanityofVariable(deviceType, 'interface_speed', interfaceL2Arg2)
        if (value == 'ok'):
            command = (command + interfaceL2Arg2)
        else:
            retVal = 'Error-225'
            return retVal
    elif (interfaceL2Arg1 == 'storm-control'):
        command = (interfaceL2Arg1 + ' ')
        value = checkSanityofVariable(deviceType, 'stormcontrol_options', interfaceL2Arg2)
        if (value == 'ok'):
            command = ((command + interfaceL2Arg2) + ' level ')
            value = checkSanityofVariable(deviceType, 'stormcontrol_level', interfaceL2Arg3)
            if (value == 'ok'):
                command = (command + interfaceL2Arg3)
            else:
                retVal = 'Error-226'
                return retVal
        else:
            retVal = 'Error-227'
            return retVal
    elif (interfaceL2Arg1 == 'vlan'):
        command = (interfaceL2Arg1 + ' dot1q tag native ')
        value = checkSanityofVariable(deviceType, 'portchannel_dot1q_tag', interfaceL2Arg2)
        if (value == 'ok'):
            command = (command + interfaceL2Arg2)
            if (interfaceL2Arg2 == 'egress-only'):
                command = (command + ' enable')
        else:
            retVal = 'Error-228'
            return retVal
    elif (interfaceL2Arg1 == 'vrrp'):
        command = (interfaceL2Arg1 + ' ')
        value = checkSanityofVariable(deviceType, 'vrrp_id', interfaceL2Arg2)
        if (value == 'ok'):
            command = ((command + interfaceL2Arg2) + ' ')
            if (interfaceL2Arg3 == 'ipv6'):
                command = ((command + interfaceL2Arg3) + ' ')
            elif (interfaceL2Arg3 is None):
                command = (command + '')
            else:
                retVal = 'Error-229'
                return retVal
        else:
            retVal = 'Error-230'
            return retVal
    else:
        retVal = 'Error-233'
        return retVal
    command = (command + '\n')
    retVal = (retVal + waitForDeviceResponse(command, prompt, timeout, obj))
    if ((prompt == '(config-if)#') or (prompt == '(config-if-range)#')):
        command = 'exit \n'
        retVal = (retVal + waitForDeviceResponse(command, '(config)#', timeout, obj))
    return retVal