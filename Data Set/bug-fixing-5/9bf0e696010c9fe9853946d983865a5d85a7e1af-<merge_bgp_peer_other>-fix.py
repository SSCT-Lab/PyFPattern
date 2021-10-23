def merge_bgp_peer_other(self, **kwargs):
    ' merge_bgp_peer '
    module = kwargs['module']
    vrf_name = module.params['vrf_name']
    peer_addr = module.params['peer_addr']
    conf_str = (CE_MERGE_BGP_PEER_HEADER % (vrf_name, peer_addr))
    cmds = []
    description = module.params['description']
    if description:
        conf_str += ('<description>%s</description>' % description)
        cmd = ('peer %s description %s' % (peer_addr, description))
        cmds.append(cmd)
    fake_as = module.params['fake_as']
    if fake_as:
        conf_str += ('<fakeAs>%s</fakeAs>' % fake_as)
        cmd = ('peer %s local-as %s' % (peer_addr, fake_as))
        cmds.append(cmd)
    dual_as = module.params['dual_as']
    if (dual_as != 'no_use'):
        conf_str += ('<dualAs>%s</dualAs>' % dual_as)
        if (dual_as == 'true'):
            cmd = ('peer %s local-as %s dual-as' % (peer_addr, fake_as))
        else:
            cmd = ('peer %s local-as %s' % (peer_addr, fake_as))
        cmds.append(cmd)
    conventional = module.params['conventional']
    if (conventional != 'no_use'):
        conf_str += ('<conventional>%s</conventional>' % conventional)
        if (conventional == 'true'):
            cmd = ('peer %s capability-advertise conventional' % peer_addr)
        else:
            cmd = ('undo peer %s capability-advertise conventional' % peer_addr)
        cmds.append(cmd)
    route_refresh = module.params['route_refresh']
    if (route_refresh != 'no_use'):
        conf_str += ('<routeRefresh>%s</routeRefresh>' % route_refresh)
        if (route_refresh == 'true'):
            cmd = ('peer %s capability-advertise route-refresh' % peer_addr)
        else:
            cmd = ('undo peer %s capability-advertise route-refresh' % peer_addr)
        cmds.append(cmd)
    four_byte_as = module.params['four_byte_as']
    if (four_byte_as != 'no_use'):
        conf_str += ('<fourByteAs>%s</fourByteAs>' % four_byte_as)
        if (four_byte_as == 'true'):
            cmd = ('peer %s capability-advertise 4-byte-as' % peer_addr)
        else:
            cmd = ('undo peer %s capability-advertise 4-byte-as' % peer_addr)
        cmds.append(cmd)
    is_ignore = module.params['is_ignore']
    if (is_ignore != 'no_use'):
        conf_str += ('<isIgnore>%s</isIgnore>' % is_ignore)
        if (is_ignore == 'true'):
            cmd = ('peer %s ignore' % peer_addr)
        else:
            cmd = ('undo peer %s ignore' % peer_addr)
        cmds.append(cmd)
    local_if_name = module.params['local_if_name']
    if local_if_name:
        conf_str += ('<localIfName>%s</localIfName>' % local_if_name)
        cmd = ('peer %s connect-interface %s' % (peer_addr, local_if_name))
        cmds.append(cmd)
    ebgp_max_hop = module.params['ebgp_max_hop']
    if ebgp_max_hop:
        conf_str += ('<ebgpMaxHop>%s</ebgpMaxHop>' % ebgp_max_hop)
        cmd = ('peer %s ebgp-max-hop %s' % (peer_addr, ebgp_max_hop))
        cmds.append(cmd)
    valid_ttl_hops = module.params['valid_ttl_hops']
    if valid_ttl_hops:
        conf_str += ('<validTtlHops>%s</validTtlHops>' % valid_ttl_hops)
        cmd = ('peer %s valid-ttl-hops %s' % (peer_addr, valid_ttl_hops))
        cmds.append(cmd)
    connect_mode = module.params['connect_mode']
    if connect_mode:
        if (connect_mode == 'listenOnly'):
            cmd = ('peer %s listen-only' % peer_addr)
            cmds.append(cmd)
        elif (connect_mode == 'connectOnly'):
            cmd = ('peer %s connect-only' % peer_addr)
            cmds.append(cmd)
        elif (connect_mode == 'both'):
            connect_mode = 'null'
            cmd = ('peer %s listen-only' % peer_addr)
            cmds.append(cmd)
            cmd = ('peer %s connect-only' % peer_addr)
            cmds.append(cmd)
        conf_str += ('<connectMode>%s</connectMode>' % connect_mode)
    is_log_change = module.params['is_log_change']
    if (is_log_change != 'no_use'):
        conf_str += ('<isLogChange>%s</isLogChange>' % is_log_change)
        if (is_log_change == 'true'):
            cmd = ('peer %s log-change' % peer_addr)
        else:
            cmd = ('undo peer %s log-change' % peer_addr)
        cmds.append(cmd)
    pswd_type = module.params['pswd_type']
    if pswd_type:
        conf_str += ('<pswdType>%s</pswdType>' % pswd_type)
    pswd_cipher_text = module.params['pswd_cipher_text']
    if pswd_cipher_text:
        conf_str += ('<pswdCipherText>%s</pswdCipherText>' % pswd_cipher_text)
        if (pswd_type == 'cipher'):
            cmd = ('peer %s password cipher %s' % (peer_addr, pswd_cipher_text))
        elif (pswd_type == 'simple'):
            cmd = ('peer %s password simple %s' % (peer_addr, pswd_cipher_text))
        cmds.append(cmd)
    keep_alive_time = module.params['keep_alive_time']
    if keep_alive_time:
        conf_str += ('<keepAliveTime>%s</keepAliveTime>' % keep_alive_time)
        cmd = ('peer %s timer keepalive %s' % (peer_addr, keep_alive_time))
        cmds.append(cmd)
    hold_time = module.params['hold_time']
    if hold_time:
        conf_str += ('<holdTime>%s</holdTime>' % hold_time)
        cmd = ('peer %s timer hold %s' % (peer_addr, hold_time))
        cmds.append(cmd)
    min_hold_time = module.params['min_hold_time']
    if min_hold_time:
        conf_str += ('<minHoldTime>%s</minHoldTime>' % min_hold_time)
        cmd = ('peer %s timer min-holdtime %s' % (peer_addr, min_hold_time))
        cmds.append(cmd)
    key_chain_name = module.params['key_chain_name']
    if key_chain_name:
        conf_str += ('<keyChainName>%s</keyChainName>' % key_chain_name)
        cmd = ('peer %s keychain %s' % (peer_addr, key_chain_name))
        cmds.append(cmd)
    conn_retry_time = module.params['conn_retry_time']
    if conn_retry_time:
        conf_str += ('<connRetryTime>%s</connRetryTime>' % conn_retry_time)
        cmd = ('peer %s timer connect-retry %s' % (peer_addr, conn_retry_time))
        cmds.append(cmd)
    tcp_mss = module.params['tcp_MSS']
    if tcp_mss:
        conf_str += ('<tcpMSS>%s</tcpMSS>' % tcp_mss)
        cmd = ('peer %s tcp-mss %s' % (peer_addr, tcp_mss))
        cmds.append(cmd)
    mpls_local_ifnet_disable = module.params['mpls_local_ifnet_disable']
    if (mpls_local_ifnet_disable != 'no_use'):
        conf_str += ('<mplsLocalIfnetDisable>%s</mplsLocalIfnetDisable>' % mpls_local_ifnet_disable)
        if (mpls_local_ifnet_disable == 'false'):
            cmd = ('undo peer %s mpls-local-ifnet disable' % peer_addr)
        else:
            cmd = ('peer %s mpls-local-ifnet disable' % peer_addr)
        cmds.append(cmd)
    prepend_global_as = module.params['prepend_global_as']
    if (prepend_global_as != 'no_use'):
        conf_str += ('<prependGlobalAs>%s</prependGlobalAs>' % prepend_global_as)
        if (prepend_global_as == 'true'):
            cmd = ('peer %s local-as %s prepend-global-as' % (peer_addr, fake_as))
        else:
            cmd = ('undo peer %s local-as %s prepend-global-as' % (peer_addr, fake_as))
        cmds.append(cmd)
    prepend_fake_as = module.params['prepend_fake_as']
    if (prepend_fake_as != 'no_use'):
        conf_str += ('<prependFakeAs>%s</prependFakeAs>' % prepend_fake_as)
        if (prepend_fake_as == 'true'):
            cmd = ('peer %s local-as %s prepend-local-as' % (peer_addr, fake_as))
        else:
            cmd = ('undo peer %s local-as %s prepend-local-as' % (peer_addr, fake_as))
        cmds.append(cmd)
    conf_str += CE_MERGE_BGP_PEER_TAIL
    recv_xml = self.netconf_set_config(module=module, conf_str=conf_str)
    if ('<ok/>' not in recv_xml):
        module.fail_json(msg='Error: Merge bgp peer other failed.')
    return cmds