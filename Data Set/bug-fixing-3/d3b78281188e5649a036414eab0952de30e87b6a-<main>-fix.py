def main():
    module_specific_arguments = dict(name=dict(type='str'), ip=dict(type='str'), servername=dict(type='str'), servicetype=dict(type='str', choices=['HTTP', 'FTP', 'TCP', 'UDP', 'SSL', 'SSL_BRIDGE', 'SSL_TCP', 'DTLS', 'NNTP', 'RPCSVR', 'DNS', 'ADNS', 'SNMP', 'RTSP', 'DHCPRA', 'ANY', 'SIP_UDP', 'SIP_TCP', 'SIP_SSL', 'DNS_TCP', 'ADNS_TCP', 'MYSQL', 'MSSQL', 'ORACLE', 'RADIUS', 'RADIUSListener', 'RDP', 'DIAMETER', 'SSL_DIAMETER', 'TFTP', 'SMPP', 'PPTP', 'GRE', 'SYSLOGTCP', 'SYSLOGUDP', 'FIX', 'SSL_FIX']), port=dict(type='int'), cleartextport=dict(type='int'), cachetype=dict(type='str', choices=['TRANSPARENT', 'REVERSE', 'FORWARD']), maxclient=dict(type='float'), healthmonitor=dict(type='bool', default=True), maxreq=dict(type='float'), cacheable=dict(type='bool', default=False), cip=dict(type='str', choices=['enabled', 'disabled']), cipheader=dict(type='str'), usip=dict(type='bool'), useproxyport=dict(type='bool'), sp=dict(type='bool'), rtspsessionidremap=dict(type='bool', default=False), clttimeout=dict(type='float'), svrtimeout=dict(type='float'), customserverid=dict(type='str', default='None'), cka=dict(type='bool'), tcpb=dict(type='bool'), cmp=dict(type='bool'), maxbandwidth=dict(type='float'), accessdown=dict(type='bool', default=False), monthreshold=dict(type='float'), downstateflush=dict(type='str', choices=['enabled', 'disabled']), tcpprofilename=dict(type='str'), httpprofilename=dict(type='str'), hashid=dict(type='float'), comment=dict(type='str'), appflowlog=dict(type='str', choices=['enabled', 'disabled']), netprofile=dict(type='str'), processlocal=dict(type='str', choices=['enabled', 'disabled']), dnsprofilename=dict(type='str'), ipaddress=dict(type='str'), graceful=dict(type='bool', default=False))
    hand_inserted_arguments = dict(monitor_bindings=dict(type='list'), disabled=dict(type='bool', default=False))
    argument_spec = dict()
    argument_spec.update(netscaler_common_arguments)
    argument_spec.update(module_specific_arguments)
    argument_spec.update(hand_inserted_arguments)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    module_result = dict(changed=False, failed=False, loglines=loglines)
    if (not PYTHON_SDK_IMPORTED):
        module.fail_json(msg='Could not load nitro python sdk')
    client = get_nitro_client(module)
    try:
        client.login()
    except nitro_exception as e:
        msg = ('nitro exception during login. errorcode=%s, message=%s' % (str(e.errorcode), e.message))
        module.fail_json(msg=msg)
    except Exception as e:
        if (str(type(e)) == "<class 'requests.exceptions.ConnectionError'>"):
            module.fail_json(msg=('Connection error %s' % str(e)))
        elif (str(type(e)) == "<class 'requests.exceptions.SSLError'>"):
            module.fail_json(msg=('SSL Error %s' % str(e)))
        else:
            module.fail_json(msg=('Unexpected error during login %s' % str(e)))
    readwrite_attrs = ['name', 'ip', 'servername', 'servicetype', 'port', 'cleartextport', 'cachetype', 'maxclient', 'healthmonitor', 'maxreq', 'cacheable', 'cip', 'cipheader', 'usip', 'useproxyport', 'sp', 'rtspsessionidremap', 'clttimeout', 'svrtimeout', 'customserverid', 'cka', 'tcpb', 'cmp', 'maxbandwidth', 'accessdown', 'monthreshold', 'downstateflush', 'tcpprofilename', 'httpprofilename', 'hashid', 'comment', 'appflowlog', 'netprofile', 'processlocal', 'dnsprofilename', 'ipaddress', 'graceful']
    readonly_attrs = ['numofconnections', 'policyname', 'serviceconftype', 'serviceconftype2', 'value', 'gslb', 'dup_state', 'publicip', 'publicport', 'svrstate', 'monitor_state', 'monstatcode', 'lastresponse', 'responsetime', 'riseapbrstatsmsgcode2', 'monstatparam1', 'monstatparam2', 'monstatparam3', 'statechangetimesec', 'statechangetimemsec', 'tickssincelaststatechange', 'stateupdatereason', 'clmonowner', 'clmonview', 'serviceipstr', 'oracleserverversion']
    immutable_attrs = ['name', 'ip', 'servername', 'servicetype', 'port', 'cleartextport', 'cachetype', 'cipheader', 'serverid', 'state', 'td', 'monitor_name_svc', 'riseapbrstatsmsgcode', 'all', 'Internal', 'newname']
    transforms = {
        'pathmonitorindv': ['bool_yes_no'],
        'cacheable': ['bool_yes_no'],
        'cka': ['bool_yes_no'],
        'pathmonitor': ['bool_yes_no'],
        'tcpb': ['bool_yes_no'],
        'sp': ['bool_on_off'],
        'graceful': ['bool_yes_no'],
        'usip': ['bool_yes_no'],
        'healthmonitor': ['bool_yes_no'],
        'useproxyport': ['bool_yes_no'],
        'rtspsessionidremap': ['bool_on_off'],
        'accessdown': ['bool_yes_no'],
        'cmp': ['bool_yes_no'],
        'cip': [(lambda v: v.upper())],
        'downstateflush': [(lambda v: v.upper())],
        'appflowlog': [(lambda v: v.upper())],
        'processlocal': [(lambda v: v.upper())],
    }
    monitor_bindings_rw_attrs = ['servicename', 'servicegroupname', 'dup_state', 'dup_weight', 'monitorname', 'weight']
    if (module.params['ip'] is None):
        module.params['ip'] = module.params['ipaddress']
    service_proxy = ConfigProxy(actual=service(), client=client, attribute_values_dict=module.params, readwrite_attrs=readwrite_attrs, readonly_attrs=readonly_attrs, immutable_attrs=immutable_attrs, transforms=transforms)
    try:
        if (module.params['state'] == 'present'):
            log('Applying actions for state present')
            if (not service_exists(client, module)):
                if (not module.check_mode):
                    service_proxy.add()
                    sync_monitor_bindings(client, module, monitor_bindings_rw_attrs)
                    if module.params['save_config']:
                        client.save_config()
                module_result['changed'] = True
            elif (not all_identical(client, module, service_proxy, monitor_bindings_rw_attrs)):
                diff_dict = diff(client, module, service_proxy)
                immutables_changed = get_immutables_intersection(service_proxy, diff_dict.keys())
                if (immutables_changed != []):
                    msg = ('Cannot update immutable attributes %s. Must delete and recreate entity.' % (immutables_changed,))
                    module.fail_json(msg=msg, diff=diff_dict, **module_result)
                if (not service_identical(client, module, service_proxy)):
                    if (not module.check_mode):
                        service_proxy.update()
                if (not monitor_bindings_identical(client, module, monitor_bindings_rw_attrs)):
                    if (not module.check_mode):
                        sync_monitor_bindings(client, module, monitor_bindings_rw_attrs)
                module_result['changed'] = True
                if (not module.check_mode):
                    if module.params['save_config']:
                        client.save_config()
            else:
                module_result['changed'] = False
            if (not module.check_mode):
                res = do_state_change(client, module, service_proxy)
                if (res.errorcode != 0):
                    msg = ('Error when setting disabled state. errorcode: %s message: %s' % (res.errorcode, res.message))
                    module.fail_json(msg=msg, **module_result)
            if (not module.check_mode):
                log('Sanity checks for state present')
                if (not service_exists(client, module)):
                    module.fail_json(msg='Service does not exist', **module_result)
                if (not service_identical(client, module, service_proxy)):
                    module.fail_json(msg='Service differs from configured', diff=diff(client, module, service_proxy), **module_result)
                if (not monitor_bindings_identical(client, module, monitor_bindings_rw_attrs)):
                    module.fail_json(msg='Monitor bindings are not identical', **module_result)
        elif (module.params['state'] == 'absent'):
            log('Applying actions for state absent')
            if service_exists(client, module):
                if (not module.check_mode):
                    service_proxy.delete()
                    if module.params['save_config']:
                        client.save_config()
                module_result['changed'] = True
            else:
                module_result['changed'] = False
            if (not module.check_mode):
                log('Sanity checks for state absent')
                if service_exists(client, module):
                    module.fail_json(msg='Service still exists', **module_result)
    except nitro_exception as e:
        msg = ('nitro exception errorcode=%s, message=%s' % (str(e.errorcode), e.message))
        module.fail_json(msg=msg, **module_result)
    client.logout()
    module.exit_json(**module_result)