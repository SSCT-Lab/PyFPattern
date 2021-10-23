def check_bgp_peer_other_args(self, **kwargs):
    ' check_bgp_peer_other_args '
    module = kwargs['module']
    result = dict()
    need_cfg = False
    peerip = module.params['peer_addr']
    vrf_name = module.params['vrf_name']
    if vrf_name:
        if ((len(vrf_name) > 31) or (len(vrf_name) == 0)):
            module.fail_json(msg=('Error: The len of vrf_name %s is out of [1 - 31].' % vrf_name))
    description = module.params['description']
    if description:
        if ((len(description) > 80) or (len(description) < 1)):
            module.fail_json(msg=('Error: The len of description %s is out of [1 - 80].' % description))
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<description></description>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<description>(.*)</description>.*', recv_xml)
            if re_find:
                result['description'] = re_find
                if (re_find[0] != description):
                    need_cfg = True
            else:
                need_cfg = True
    fake_as = module.params['fake_as']
    if fake_as:
        if ((len(fake_as) > 11) or (len(fake_as) < 1)):
            module.fail_json(msg=('Error: The len of fake_as %s is out of [1 - 11].' % fake_as))
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<fakeAs></fakeAs>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<fakeAs>(.*)</fakeAs>.*', recv_xml)
            if re_find:
                result['fake_as'] = re_find
                if (re_find[0] != fake_as):
                    need_cfg = True
            else:
                need_cfg = True
    dual_as = module.params['dual_as']
    if (dual_as != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<dualAs></dualAs>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<dualAs>(.*)</dualAs>.*', recv_xml)
            if re_find:
                result['dual_as'] = re_find
                if (re_find[0] != dual_as):
                    need_cfg = True
            else:
                need_cfg = True
    conventional = module.params['conventional']
    if (conventional != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<conventional></conventional>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<conventional>(.*)</conventional>.*', recv_xml)
            if re_find:
                result['conventional'] = re_find
                if (re_find[0] != conventional):
                    need_cfg = True
            else:
                need_cfg = True
    route_refresh = module.params['route_refresh']
    if (route_refresh != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<routeRefresh></routeRefresh>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<routeRefresh>(.*)</routeRefresh>.*', recv_xml)
            if re_find:
                result['route_refresh'] = re_find
                if (re_find[0] != route_refresh):
                    need_cfg = True
            else:
                need_cfg = True
    four_byte_as = module.params['four_byte_as']
    if (four_byte_as != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<fourByteAs></fourByteAs>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<fourByteAs>(.*)</fourByteAs>.*', recv_xml)
            if re_find:
                result['four_byte_as'] = re_find
                if (re_find[0] != four_byte_as):
                    need_cfg = True
            else:
                need_cfg = True
    is_ignore = module.params['is_ignore']
    if (is_ignore != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<isIgnore></isIgnore>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<isIgnore>(.*)</isIgnore>.*', recv_xml)
            if re_find:
                result['is_ignore'] = re_find
                if (re_find[0] != is_ignore):
                    need_cfg = True
            else:
                need_cfg = True
    local_if_name = module.params['local_if_name']
    if local_if_name:
        if ((len(local_if_name) > 63) or (len(local_if_name) < 1)):
            module.fail_json(msg=('Error: The len of local_if_name %s is out of [1 - 63].' % local_if_name))
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<localIfName></localIfName>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<localIfName>(.*)</localIfName>.*', recv_xml)
            if re_find:
                result['local_if_name'] = re_find
                if (re_find[0].lower() != local_if_name.lower()):
                    need_cfg = True
            else:
                need_cfg = True
    ebgp_max_hop = module.params['ebgp_max_hop']
    if ebgp_max_hop:
        if ((int(ebgp_max_hop) > 255) or (int(ebgp_max_hop) < 1)):
            module.fail_json(msg=('Error: The value of ebgp_max_hop %s is out of [1 - 255].' % ebgp_max_hop))
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<ebgpMaxHop></ebgpMaxHop>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<ebgpMaxHop>(.*)</ebgpMaxHop>.*', recv_xml)
            if re_find:
                result['ebgp_max_hop'] = re_find
                if (re_find[0] != ebgp_max_hop):
                    need_cfg = True
            else:
                need_cfg = True
    valid_ttl_hops = module.params['valid_ttl_hops']
    if valid_ttl_hops:
        if ((int(valid_ttl_hops) > 255) or (int(valid_ttl_hops) < 1)):
            module.fail_json(msg=('Error: The value of valid_ttl_hops %s is out of [1 - 255].' % valid_ttl_hops))
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<validTtlHops></validTtlHops>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<validTtlHops>(.*)</validTtlHops>.*', recv_xml)
            if re_find:
                result['valid_ttl_hops'] = re_find
                if (re_find[0] != valid_ttl_hops):
                    need_cfg = True
            else:
                need_cfg = True
    connect_mode = module.params['connect_mode']
    if connect_mode:
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<connectMode></connectMode>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<connectMode>(.*)</connectMode>.*', recv_xml)
            if re_find:
                result['connect_mode'] = re_find
                if (re_find[0] != connect_mode):
                    need_cfg = True
            else:
                need_cfg = True
    is_log_change = module.params['is_log_change']
    if (is_log_change != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<isLogChange></isLogChange>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<isLogChange>(.*)</isLogChange>.*', recv_xml)
            if re_find:
                result['is_log_change'] = re_find
                if (re_find[0] != is_log_change):
                    need_cfg = True
            else:
                need_cfg = True
    pswd_type = module.params['pswd_type']
    if pswd_type:
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<pswdType></pswdType>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<pswdType>(.*)</pswdType>.*', recv_xml)
            if re_find:
                result['pswd_type'] = re_find
                if (re_find[0] != pswd_type):
                    need_cfg = True
            else:
                need_cfg = True
    pswd_cipher_text = module.params['pswd_cipher_text']
    if pswd_cipher_text:
        if ((len(pswd_cipher_text) > 255) or (len(pswd_cipher_text) < 1)):
            module.fail_json(msg=('Error: The len of pswd_cipher_text %s is out of [1 - 255].' % pswd_cipher_text))
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<pswdCipherText></pswdCipherText>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<pswdCipherText>(.*)</pswdCipherText>.*', recv_xml)
            if re_find:
                result['pswd_cipher_text'] = re_find
                if (re_find[0] != pswd_cipher_text):
                    need_cfg = True
            else:
                need_cfg = True
    keep_alive_time = module.params['keep_alive_time']
    if keep_alive_time:
        if ((int(keep_alive_time) > 21845) or (len(keep_alive_time) < 0)):
            module.fail_json(msg=('Error: The len of keep_alive_time %s is out of [0 - 21845].' % keep_alive_time))
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<keepAliveTime></keepAliveTime>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<keepAliveTime>(.*)</keepAliveTime>.*', recv_xml)
            if re_find:
                result['keep_alive_time'] = re_find
                if (re_find[0] != keep_alive_time):
                    need_cfg = True
            else:
                need_cfg = True
    hold_time = module.params['hold_time']
    if hold_time:
        if ((int(hold_time) != 0) and ((int(hold_time) > 65535) or (int(hold_time) < 3))):
            module.fail_json(msg=('Error: The value of hold_time %s is out of [0 or 3 - 65535].' % hold_time))
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<holdTime></holdTime>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<holdTime>(.*)</holdTime>.*', recv_xml)
            if re_find:
                result['hold_time'] = re_find
                if (re_find[0] != hold_time):
                    need_cfg = True
            else:
                need_cfg = True
    min_hold_time = module.params['min_hold_time']
    if min_hold_time:
        if ((int(min_hold_time) != 0) and ((int(min_hold_time) > 65535) or (int(min_hold_time) < 20))):
            module.fail_json(msg=('Error: The value of min_hold_time %s is out of [0 or 20 - 65535].' % min_hold_time))
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<minHoldTime></minHoldTime>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<minHoldTime>(.*)</minHoldTime>.*', recv_xml)
            if re_find:
                result['min_hold_time'] = re_find
                if (re_find[0] != min_hold_time):
                    need_cfg = True
            else:
                need_cfg = True
    key_chain_name = module.params['key_chain_name']
    if key_chain_name:
        if ((len(key_chain_name) > 47) or (len(key_chain_name) < 1)):
            module.fail_json(msg=('Error: The len of key_chain_name %s is out of [1 - 47].' % key_chain_name))
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<keyChainName></keyChainName>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<keyChainName>(.*)</keyChainName>.*', recv_xml)
            if re_find:
                result['key_chain_name'] = re_find
                if (re_find[0] != key_chain_name):
                    need_cfg = True
            else:
                need_cfg = True
    conn_retry_time = module.params['conn_retry_time']
    if conn_retry_time:
        if ((int(conn_retry_time) > 65535) or (int(conn_retry_time) < 1)):
            module.fail_json(msg=('Error: The value of conn_retry_time %s is out of [1 - 65535].' % conn_retry_time))
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<connRetryTime></connRetryTime>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<connRetryTime>(.*)</connRetryTime>.*', recv_xml)
            if re_find:
                result['conn_retry_time'] = re_find
                if (re_find[0] != conn_retry_time):
                    need_cfg = True
            else:
                need_cfg = True
    tcp_mss = module.params['tcp_MSS']
    if tcp_mss:
        if ((int(tcp_mss) > 4096) or (int(tcp_mss) < 176)):
            module.fail_json(msg=('Error: The value of tcp_mss %s is out of [176 - 4096].' % tcp_mss))
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<tcpMSS></tcpMSS>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<tcpMSS>(.*)</tcpMSS>.*', recv_xml)
            if re_find:
                result['tcp_MSS'] = re_find
                if (re_find[0] != tcp_mss):
                    need_cfg = True
            else:
                need_cfg = True
    mpls_local_ifnet_disable = module.params['mpls_local_ifnet_disable']
    if (mpls_local_ifnet_disable != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<mplsLocalIfnetDisable></mplsLocalIfnetDisable>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<mplsLocalIfnetDisable>(.*)</mplsLocalIfnetDisable>.*', recv_xml)
            if re_find:
                result['mpls_local_ifnet_disable'] = re_find
                if (re_find[0] != mpls_local_ifnet_disable):
                    need_cfg = True
            else:
                need_cfg = True
    prepend_global_as = module.params['prepend_global_as']
    if (prepend_global_as != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<prependGlobalAs></prependGlobalAs>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<prependGlobalAs>(.*)</prependGlobalAs>.*', recv_xml)
            if re_find:
                result['prepend_global_as'] = re_find
                if (re_find[0] != prepend_global_as):
                    need_cfg = True
            else:
                need_cfg = True
    prepend_fake_as = module.params['prepend_fake_as']
    if (prepend_fake_as != 'no_use'):
        conf_str = (((CE_GET_BGP_PEER_HEADER % (vrf_name, peerip)) + '<prependFakeAs></prependFakeAs>') + CE_GET_BGP_PEER_TAIL)
        recv_xml = self.netconf_get_config(module=module, conf_str=conf_str)
        if ('<data/>' in recv_xml):
            need_cfg = True
        else:
            re_find = re.findall('.*<prependFakeAs>(.*)</prependFakeAs>.*', recv_xml)
            if re_find:
                result['prepend_fake_as'] = re_find
                if (re_find[0] != prepend_fake_as):
                    need_cfg = True
            else:
                need_cfg = True
    result['need_cfg'] = need_cfg
    return result