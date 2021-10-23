def main():
    module = AnsibleModule(argument_spec=dict(host=dict(required=True), version=dict(required=True, choices=['v2', 'v2c', 'v3']), community=dict(required=False, default=False), username=dict(required=False), level=dict(required=False, choices=['authNoPriv', 'authPriv']), integrity=dict(required=False, choices=['md5', 'sha']), privacy=dict(required=False, choices=['des', 'aes']), authkey=dict(required=False), privkey=dict(required=False), removeplaceholder=dict(required=False)), required_together=(['username', 'level', 'integrity', 'authkey'], ['privacy', 'privkey']), supports_check_mode=False)
    m_args = module.params
    if (not has_pysnmp):
        module.fail_json(msg='Missing required pysnmp module (check docs)')
    cmdGen = cmdgen.CommandGenerator()
    if ((m_args['version'] == 'v2') or (m_args['version'] == 'v2c')):
        if (m_args['community'] is False):
            module.fail_json(msg='Community not set when using snmp version 2')
    if (m_args['version'] == 'v3'):
        if (m_args['username'] is None):
            module.fail_json(msg='Username not set when using snmp version 3')
        if ((m_args['level'] == 'authPriv') and (m_args['privacy'] is None)):
            module.fail_json(msg='Privacy algorithm not set when using authPriv')
        if (m_args['integrity'] == 'sha'):
            integrity_proto = cmdgen.usmHMACSHAAuthProtocol
        elif (m_args['integrity'] == 'md5'):
            integrity_proto = cmdgen.usmHMACMD5AuthProtocol
        if (m_args['privacy'] == 'aes'):
            privacy_proto = cmdgen.usmAesCfb128Protocol
        elif (m_args['privacy'] == 'des'):
            privacy_proto = cmdgen.usmDESPrivProtocol
    if ((m_args['version'] == 'v2') or (m_args['version'] == 'v2c')):
        snmp_auth = cmdgen.CommunityData(m_args['community'])
    elif (m_args['level'] == 'authNoPriv'):
        snmp_auth = cmdgen.UsmUserData(m_args['username'], authKey=m_args['authkey'], authProtocol=integrity_proto)
    else:
        snmp_auth = cmdgen.UsmUserData(m_args['username'], authKey=m_args['authkey'], privKey=m_args['privkey'], authProtocol=integrity_proto, privProtocol=privacy_proto)
    p = DefineOid(dotprefix=True)
    v = DefineOid(dotprefix=False)

    def Tree():
        return defaultdict(Tree)
    results = Tree()
    (errorIndication, errorStatus, errorIndex, varBinds) = cmdGen.getCmd(snmp_auth, cmdgen.UdpTransportTarget((m_args['host'], 161)), cmdgen.MibVariable(p.sysDescr), cmdgen.MibVariable(p.sysObjectId), cmdgen.MibVariable(p.sysUpTime), cmdgen.MibVariable(p.sysContact), cmdgen.MibVariable(p.sysName), cmdgen.MibVariable(p.sysLocation), lookupMib=False)
    if errorIndication:
        module.fail_json(msg=str(errorIndication))
    for (oid, val) in varBinds:
        current_oid = oid.prettyPrint()
        current_val = val.prettyPrint()
        if (current_oid == v.sysDescr):
            results['ansible_sysdescr'] = decode_hex(current_val)
        elif (current_oid == v.sysObjectId):
            results['ansible_sysobjectid'] = current_val
        elif (current_oid == v.sysUpTime):
            results['ansible_sysuptime'] = current_val
        elif (current_oid == v.sysContact):
            results['ansible_syscontact'] = current_val
        elif (current_oid == v.sysName):
            results['ansible_sysname'] = current_val
        elif (current_oid == v.sysLocation):
            results['ansible_syslocation'] = current_val
    (errorIndication, errorStatus, errorIndex, varTable) = cmdGen.nextCmd(snmp_auth, cmdgen.UdpTransportTarget((m_args['host'], 161)), cmdgen.MibVariable(p.ifIndex), cmdgen.MibVariable(p.ifDescr), cmdgen.MibVariable(p.ifMtu), cmdgen.MibVariable(p.ifSpeed), cmdgen.MibVariable(p.ifPhysAddress), cmdgen.MibVariable(p.ifAdminStatus), cmdgen.MibVariable(p.ifOperStatus), cmdgen.MibVariable(p.ipAdEntAddr), cmdgen.MibVariable(p.ipAdEntIfIndex), cmdgen.MibVariable(p.ipAdEntNetMask), cmdgen.MibVariable(p.ifAlias), lookupMib=False)
    if errorIndication:
        module.fail_json(msg=str(errorIndication))
    interface_indexes = []
    all_ipv4_addresses = []
    ipv4_networks = Tree()
    for varBinds in varTable:
        for (oid, val) in varBinds:
            current_oid = oid.prettyPrint()
            current_val = val.prettyPrint()
            if (v.ifIndex in current_oid):
                ifIndex = int(current_oid.rsplit('.', 1)[(- 1)])
                results['ansible_interfaces'][ifIndex]['ifindex'] = current_val
                interface_indexes.append(ifIndex)
            if (v.ifDescr in current_oid):
                ifIndex = int(current_oid.rsplit('.', 1)[(- 1)])
                results['ansible_interfaces'][ifIndex]['name'] = current_val
            if (v.ifMtu in current_oid):
                ifIndex = int(current_oid.rsplit('.', 1)[(- 1)])
                results['ansible_interfaces'][ifIndex]['mtu'] = current_val
            if (v.ifMtu in current_oid):
                ifIndex = int(current_oid.rsplit('.', 1)[(- 1)])
                results['ansible_interfaces'][ifIndex]['speed'] = current_val
            if (v.ifPhysAddress in current_oid):
                ifIndex = int(current_oid.rsplit('.', 1)[(- 1)])
                results['ansible_interfaces'][ifIndex]['mac'] = decode_mac(current_val)
            if (v.ifAdminStatus in current_oid):
                ifIndex = int(current_oid.rsplit('.', 1)[(- 1)])
                results['ansible_interfaces'][ifIndex]['adminstatus'] = lookup_adminstatus(int(current_val))
            if (v.ifOperStatus in current_oid):
                ifIndex = int(current_oid.rsplit('.', 1)[(- 1)])
                results['ansible_interfaces'][ifIndex]['operstatus'] = lookup_operstatus(int(current_val))
            if (v.ipAdEntAddr in current_oid):
                curIPList = current_oid.rsplit('.', 4)[(- 4):]
                curIP = '.'.join(curIPList)
                ipv4_networks[curIP]['address'] = current_val
                all_ipv4_addresses.append(current_val)
            if (v.ipAdEntIfIndex in current_oid):
                curIPList = current_oid.rsplit('.', 4)[(- 4):]
                curIP = '.'.join(curIPList)
                ipv4_networks[curIP]['interface'] = current_val
            if (v.ipAdEntNetMask in current_oid):
                curIPList = current_oid.rsplit('.', 4)[(- 4):]
                curIP = '.'.join(curIPList)
                ipv4_networks[curIP]['netmask'] = current_val
            if (v.ifAlias in current_oid):
                ifIndex = int(current_oid.rsplit('.', 1)[(- 1)])
                results['ansible_interfaces'][ifIndex]['description'] = current_val
    interface_to_ipv4 = {
        
    }
    for ipv4_network in ipv4_networks:
        current_interface = ipv4_networks[ipv4_network]['interface']
        current_network = {
            'address': ipv4_networks[ipv4_network]['address'],
            'netmask': ipv4_networks[ipv4_network]['netmask'],
        }
        if (current_interface not in interface_to_ipv4):
            interface_to_ipv4[current_interface] = []
            interface_to_ipv4[current_interface].append(current_network)
        else:
            interface_to_ipv4[current_interface].append(current_network)
    for interface in interface_to_ipv4:
        results['ansible_interfaces'][int(interface)]['ipv4'] = interface_to_ipv4[interface]
    results['ansible_all_ipv4_addresses'] = all_ipv4_addresses
    module.exit_json(ansible_facts=results)