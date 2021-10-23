def check_advance_rule_args(self):
    ' Check advance rule invalid args '
    need_cfg = False
    find_flag = False
    self.cur_advance_rule_cfg['adv_rule_info'] = []
    if self.acl_name:
        if (self.state == 'absent'):
            if (not self.rule_name):
                self.module.fail_json(msg='Error: Please input rule_name when state is absent.')
        if self.rule_name:
            if ((len(self.rule_name) < 1) or (len(self.rule_name) > 32)):
                self.module.fail_json(msg='Error: The len of rule_name is out of [1 - 32].')
            if ((self.state != 'delete_acl') and (not self.rule_id)):
                self.module.fail_json(msg='Error: Please input rule_id.')
            if self.rule_id:
                if self.rule_id.isdigit():
                    if ((int(self.rule_id) < 0) or (int(self.rule_id) > 4294967294)):
                        self.module.fail_json(msg='Error: The value of rule_id is out of [0 - 4294967294].')
                else:
                    self.module.fail_json(msg='Error: The rule_id is not digit.')
            if (self.rule_action and (not self.protocol)):
                self.module.fail_json(msg='Error: The rule_action and the protocol must input at the same time.')
            if ((not self.rule_action) and self.protocol):
                self.module.fail_json(msg='Error: The rule_action and the protocol must input at the same time.')
            if self.protocol:
                self.get_protocol_num()
            if self.source_ip:
                if (not check_ip_addr(self.source_ip)):
                    self.module.fail_json(msg=('Error: The source_ip %s is invalid.' % self.source_ip))
                if (not self.src_mask):
                    self.module.fail_json(msg='Error: Please input src_mask.')
            if self.src_mask:
                if self.src_mask.isdigit():
                    if ((int(self.src_mask) < 1) or (int(self.src_mask) > 32)):
                        self.module.fail_json(msg='Error: The value of src_mask is out of [1 - 32].')
                    self.src_wild = get_wildcard_mask(self.src_mask)
                else:
                    self.module.fail_json(msg='Error: The src_mask is not digit.')
            if self.src_pool_name:
                if ((len(self.src_pool_name) < 1) or (len(self.src_pool_name) > 32)):
                    self.module.fail_json(msg='Error: The len of src_pool_name is out of [1 - 32].')
            if self.dest_ip:
                if (not check_ip_addr(self.dest_ip)):
                    self.module.fail_json(msg=('Error: The dest_ip %s is invalid.' % self.dest_ip))
                if (not self.dest_mask):
                    self.module.fail_json(msg='Error: Please input dest_mask.')
            if self.dest_mask:
                if self.dest_mask.isdigit():
                    if ((int(self.dest_mask) < 1) or (int(self.dest_mask) > 32)):
                        self.module.fail_json(msg='Error: The value of dest_mask is out of [1 - 32].')
                    self.dest_wild = get_wildcard_mask(self.dest_mask)
                else:
                    self.module.fail_json(msg='Error: The dest_mask is not digit.')
            if self.dest_pool_name:
                if ((len(self.dest_pool_name) < 1) or (len(self.dest_pool_name) > 32)):
                    self.module.fail_json(msg='Error: The len of dest_pool_name is out of [1 - 32].')
            if self.src_port_op:
                if (self.src_port_op == 'lt'):
                    if (not self.src_port_end):
                        self.module.fail_json(msg='Error: The src_port_end must input.')
                    if self.src_port_begin:
                        self.module.fail_json(msg='Error: The src_port_begin should not input.')
                if ((self.src_port_op == 'eq') or (self.src_port_op == 'gt')):
                    if (not self.src_port_begin):
                        self.module.fail_json(msg='Error: The src_port_begin must input.')
                    if self.src_port_end:
                        self.module.fail_json(msg='Error: The src_port_end should not input.')
                if (self.src_port_op == 'range'):
                    if ((not self.src_port_begin) or (not self.src_port_end)):
                        self.module.fail_json(msg='Error: The src_port_begin and src_port_end must input.')
            if self.src_port_begin:
                if self.src_port_begin.isdigit():
                    if ((int(self.src_port_begin) < 0) or (int(self.src_port_begin) > 65535)):
                        self.module.fail_json(msg='Error: The value of src_port_begin is out of [0 - 65535].')
                else:
                    self.module.fail_json(msg='Error: The src_port_begin is not digit.')
            if self.src_port_end:
                if self.src_port_end.isdigit():
                    if ((int(self.src_port_end) < 0) or (int(self.src_port_end) > 65535)):
                        self.module.fail_json(msg='Error: The value of src_port_end is out of [0 - 65535].')
                else:
                    self.module.fail_json(msg='Error: The src_port_end is not digit.')
            if self.src_port_pool_name:
                if ((len(self.src_port_pool_name) < 1) or (len(self.src_port_pool_name) > 32)):
                    self.module.fail_json(msg='Error: The len of src_port_pool_name is out of [1 - 32].')
            if self.dest_port_op:
                if (self.dest_port_op == 'lt'):
                    if (not self.dest_port_end):
                        self.module.fail_json(msg='Error: The dest_port_end must input.')
                    if self.dest_port_begin:
                        self.module.fail_json(msg='Error: The dest_port_begin should not input.')
                if ((self.dest_port_op == 'eq') or (self.dest_port_op == 'gt')):
                    if (not self.dest_port_begin):
                        self.module.fail_json(msg='Error: The dest_port_begin must input.')
                    if self.dest_port_end:
                        self.module.fail_json(msg='Error: The dest_port_end should not input.')
                if (self.dest_port_op == 'range'):
                    if ((not self.dest_port_begin) or (not self.dest_port_end)):
                        self.module.fail_json(msg='Error: The dest_port_begin and dest_port_end must input.')
            if self.dest_port_begin:
                if self.dest_port_begin.isdigit():
                    if ((int(self.dest_port_begin) < 0) or (int(self.dest_port_begin) > 65535)):
                        self.module.fail_json(msg='Error: The value of dest_port_begin is out of [0 - 65535].')
                else:
                    self.module.fail_json(msg='Error: The dest_port_begin is not digit.')
            if self.dest_port_end:
                if self.dest_port_end.isdigit():
                    if ((int(self.dest_port_end) < 0) or (int(self.dest_port_end) > 65535)):
                        self.module.fail_json(msg='Error: The value of dest_port_end is out of [0 - 65535].')
                else:
                    self.module.fail_json(msg='Error: The dest_port_end is not digit.')
            if self.dest_port_pool_name:
                if ((len(self.dest_port_pool_name) < 1) or (len(self.dest_port_pool_name) > 32)):
                    self.module.fail_json(msg='Error: The len of dest_port_pool_name is out of [1 - 32].')
            if self.precedence:
                if self.precedence.isdigit():
                    if ((int(self.precedence) < 0) or (int(self.precedence) > 7)):
                        self.module.fail_json(msg='Error: The value of precedence is out of [0 - 7].')
                else:
                    self.module.fail_json(msg='Error: The precedence is not digit.')
            if self.tos:
                if self.tos.isdigit():
                    if ((int(self.tos) < 0) or (int(self.tos) > 15)):
                        self.module.fail_json(msg='Error: The value of tos is out of [0 - 15].')
                else:
                    self.module.fail_json(msg='Error: The tos is not digit.')
            if self.dscp:
                if self.dscp.isdigit():
                    if ((int(self.dscp) < 0) or (int(self.dscp) > 63)):
                        self.module.fail_json(msg='Error: The value of dscp is out of [0 - 63].')
                else:
                    self.module.fail_json(msg='Error: The dscp is not digit.')
            if self.icmp_type:
                if self.icmp_type.isdigit():
                    if ((int(self.icmp_type) < 0) or (int(self.icmp_type) > 255)):
                        self.module.fail_json(msg='Error: The value of icmp_type is out of [0 - 255].')
                else:
                    self.module.fail_json(msg='Error: The icmp_type is not digit.')
            if self.icmp_code:
                if self.icmp_code.isdigit():
                    if ((int(self.icmp_code) < 0) or (int(self.icmp_code) > 255)):
                        self.module.fail_json(msg='Error: The value of icmp_code is out of [0 - 255].')
                else:
                    self.module.fail_json(msg='Error: The icmp_code is not digit.')
            if self.vrf_name:
                if ((len(self.vrf_name) < 1) or (len(self.vrf_name) > 31)):
                    self.module.fail_json(msg='Error: The len of vrf_name is out of [1 - 31].')
            if self.syn_flag:
                if self.syn_flag.isdigit():
                    if ((int(self.syn_flag) < 0) or (int(self.syn_flag) > 63)):
                        self.module.fail_json(msg='Error: The value of syn_flag is out of [0 - 63].')
                else:
                    self.module.fail_json(msg='Error: The syn_flag is not digit.')
            if self.tcp_flag_mask:
                if self.tcp_flag_mask.isdigit():
                    if ((int(self.tcp_flag_mask) < 0) or (int(self.tcp_flag_mask) > 63)):
                        self.module.fail_json(msg='Error: The value of tcp_flag_mask is out of [0 - 63].')
                else:
                    self.module.fail_json(msg='Error: The tcp_flag_mask is not digit.')
            if self.time_range:
                if ((len(self.time_range) < 1) or (len(self.time_range) > 32)):
                    self.module.fail_json(msg='Error: The len of time_range is out of [1 - 32].')
            if self.rule_description:
                if ((len(self.rule_description) < 1) or (len(self.rule_description) > 127)):
                    self.module.fail_json(msg='Error: The len of rule_description is out of [1 - 127].')
            if self.igmp_type:
                self.get_igmp_type_num()
            conf_str = (CE_GET_ACL_ADVANCE_RULE_HEADER % self.acl_name)
            if self.rule_id:
                conf_str += '<aclRuleID></aclRuleID>'
            if self.rule_action:
                conf_str += '<aclAction></aclAction>'
            if self.protocol:
                conf_str += '<aclProtocol></aclProtocol>'
            if self.source_ip:
                conf_str += '<aclSourceIp></aclSourceIp>'
            if self.src_wild:
                conf_str += '<aclSrcWild></aclSrcWild>'
            if self.src_pool_name:
                conf_str += '<aclSPoolName></aclSPoolName>'
            if self.dest_ip:
                conf_str += '<aclDestIp></aclDestIp>'
            if self.dest_wild:
                conf_str += '<aclDestWild></aclDestWild>'
            if self.dest_pool_name:
                conf_str += '<aclDPoolName></aclDPoolName>'
            if self.src_port_op:
                conf_str += '<aclSrcPortOp></aclSrcPortOp>'
            if self.src_port_begin:
                conf_str += '<aclSrcPortBegin></aclSrcPortBegin>'
            if self.src_port_end:
                conf_str += '<aclSrcPortEnd></aclSrcPortEnd>'
            if self.src_port_pool_name:
                conf_str += '<aclSPortPoolName></aclSPortPoolName>'
            if self.dest_port_op:
                conf_str += '<aclDestPortOp></aclDestPortOp>'
            if self.dest_port_begin:
                conf_str += '<aclDestPortB></aclDestPortB>'
            if self.dest_port_end:
                conf_str += '<aclDestPortE></aclDestPortE>'
            if self.dest_port_pool_name:
                conf_str += '<aclDPortPoolName></aclDPortPoolName>'
            if self.frag_type:
                conf_str += '<aclFragType></aclFragType>'
            if self.precedence:
                conf_str += '<aclPrecedence></aclPrecedence>'
            if self.tos:
                conf_str += '<aclTos></aclTos>'
            if self.dscp:
                conf_str += '<aclDscp></aclDscp>'
            if self.icmp_name:
                conf_str += '<aclIcmpName></aclIcmpName>'
            if self.icmp_type:
                conf_str += '<aclIcmpType></aclIcmpType>'
            if self.icmp_code:
                conf_str += '<aclIcmpCode></aclIcmpCode>'
            conf_str += '<aclTtlExpired></aclTtlExpired>'
            if self.vrf_name:
                conf_str += '<vrfName></vrfName>'
            if self.syn_flag:
                conf_str += '<aclSynFlag></aclSynFlag>'
            if self.tcp_flag_mask:
                conf_str += '<aclTcpFlagMask></aclTcpFlagMask>'
            conf_str += '<aclEstablished></aclEstablished>'
            if self.time_range:
                conf_str += '<aclTimeName></aclTimeName>'
            if self.rule_description:
                conf_str += '<aclRuleDescription></aclRuleDescription>'
            if self.igmp_type:
                conf_str += '<aclIgmpType></aclIgmpType>'
            conf_str += '<aclLogFlag></aclLogFlag>'
            conf_str += CE_GET_ACL_ADVANCE_RULE_TAIL
            recv_xml = self.netconf_get_config(conf_str=conf_str)
            if ('<data/>' in recv_xml):
                find_flag = False
            else:
                xml_str = recv_xml.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
                root = ElementTree.fromstring(xml_str)
                adv_rule_info = root.findall('acl/aclGroups/aclGroup/aclRuleAdv4s/aclRuleAdv4')
                if adv_rule_info:
                    for tmp in adv_rule_info:
                        tmp_dict = dict()
                        for site in tmp:
                            if (site.tag in ['aclRuleName', 'aclRuleID', 'aclAction', 'aclProtocol', 'aclSourceIp', 'aclSrcWild', 'aclSPoolName', 'aclDestIp', 'aclDestWild', 'aclDPoolName', 'aclSrcPortOp', 'aclSrcPortBegin', 'aclSrcPortEnd', 'aclSPortPoolName', 'aclDestPortOp', 'aclDestPortB', 'aclDestPortE', 'aclDPortPoolName', 'aclFragType', 'aclPrecedence', 'aclTos', 'aclDscp', 'aclIcmpName', 'aclIcmpType', 'aclIcmpCode', 'aclTtlExpired', 'vrfName', 'aclSynFlag', 'aclTcpFlagMask', 'aclEstablished', 'aclTimeName', 'aclRuleDescription', 'aclIgmpType', 'aclLogFlag']):
                                tmp_dict[site.tag] = site.text
                        self.cur_advance_rule_cfg['adv_rule_info'].append(tmp_dict)
                if self.cur_advance_rule_cfg['adv_rule_info']:
                    for tmp in self.cur_advance_rule_cfg['adv_rule_info']:
                        find_flag = True
                        if (self.rule_name and (tmp.get('aclRuleName') != self.rule_name)):
                            find_flag = False
                        if (self.rule_id and (tmp.get('aclRuleID') != self.rule_id)):
                            find_flag = False
                        if (self.rule_action and (tmp.get('aclAction') != self.rule_action)):
                            find_flag = False
                        if (self.protocol and (tmp.get('aclProtocol') != self.protocol_num)):
                            find_flag = False
                        if self.source_ip:
                            tmp_src_ip = self.source_ip.split('.')
                            tmp_src_wild = self.src_wild.split('.')
                            tmp_addr_item = []
                            for idx in range(4):
                                item1 = (255 - int(tmp_src_wild[idx]))
                                item2 = (item1 & int(tmp_src_ip[idx]))
                                tmp_addr_item.append(item2)
                            tmp_addr = ('%s.%s.%s.%s' % (tmp_addr_item[0], tmp_addr_item[1], tmp_addr_item[2], tmp_addr_item[3]))
                            if (tmp_addr != tmp.get('aclSourceIp')):
                                find_flag = False
                        if (self.src_wild and (tmp.get('aclSrcWild') != self.src_wild)):
                            find_flag = False
                        if (self.src_pool_name and (tmp.get('aclSPoolName') != self.src_pool_name)):
                            find_flag = False
                        if self.dest_ip:
                            tmp_src_ip = self.dest_ip.split('.')
                            tmp_src_wild = self.dest_wild.split('.')
                            tmp_addr_item = []
                            for idx in range(4):
                                item1 = (255 - int(tmp_src_wild[idx]))
                                item2 = (item1 & int(tmp_src_ip[idx]))
                                tmp_addr_item.append(item2)
                            tmp_addr = ('%s.%s.%s.%s' % (tmp_addr_item[0], tmp_addr_item[1], tmp_addr_item[2], tmp_addr_item[3]))
                            if (tmp_addr != tmp.get('aclDestIp')):
                                find_flag = False
                        if (self.dest_wild and (tmp.get('aclDestWild') != self.dest_wild)):
                            find_flag = False
                        if (self.dest_pool_name and (tmp.get('aclDPoolName') != self.dest_pool_name)):
                            find_flag = False
                        if (self.src_port_op and (tmp.get('aclSrcPortOp') != self.src_port_op)):
                            find_flag = False
                        if (self.src_port_begin and (tmp.get('aclSrcPortBegin') != self.src_port_begin)):
                            find_flag = False
                        if (self.src_port_end and (tmp.get('aclSrcPortEnd') != self.src_port_end)):
                            find_flag = False
                        if (self.src_port_pool_name and (tmp.get('aclSPortPoolName') != self.src_port_pool_name)):
                            find_flag = False
                        if (self.dest_port_op and (tmp.get('aclDestPortOp') != self.dest_port_op)):
                            find_flag = False
                        if (self.dest_port_begin and (tmp.get('aclDestPortB') != self.dest_port_begin)):
                            find_flag = False
                        if (self.dest_port_end and (tmp.get('aclDestPortE') != self.dest_port_end)):
                            find_flag = False
                        if (self.dest_port_pool_name and (tmp.get('aclDPortPoolName') != self.dest_port_pool_name)):
                            find_flag = False
                        frag_type = ('clear_fragment' if (tmp.get('aclFragType') is None) else tmp.get('aclFragType'))
                        if (self.frag_type and (frag_type != self.frag_type)):
                            find_flag = False
                        if (self.precedence and (tmp.get('aclPrecedence') != self.precedence)):
                            find_flag = False
                        if (self.tos and (tmp.get('aclTos') != self.tos)):
                            find_flag = False
                        if (self.dscp and (tmp.get('aclDscp') != self.dscp)):
                            find_flag = False
                        if (self.icmp_name and (tmp.get('aclIcmpName') != self.icmp_name)):
                            find_flag = False
                        if (self.icmp_type and (tmp.get('aclIcmpType') != self.icmp_type)):
                            find_flag = False
                        if (self.icmp_code and (tmp.get('aclIcmpCode') != self.icmp_code)):
                            find_flag = False
                        if (tmp.get('aclTtlExpired').lower() != str(self.ttl_expired).lower()):
                            find_flag = False
                        if (self.vrf_name and (tmp.get('vrfName') != self.vrf_name)):
                            find_flag = False
                        if (self.syn_flag and (tmp.get('aclSynFlag') != self.syn_flag)):
                            find_flag = False
                        if (self.tcp_flag_mask and (tmp.get('aclTcpFlagMask') != self.tcp_flag_mask)):
                            find_flag = False
                        if ((self.protocol == 'tcp') and (tmp.get('aclEstablished').lower() != str(self.established).lower())):
                            find_flag = False
                        if (self.time_range and (tmp.get('aclTimeName') != self.time_range)):
                            find_flag = False
                        if (self.rule_description and (tmp.get('aclRuleDescription') != self.rule_description)):
                            find_flag = False
                        if (self.igmp_type and (tmp.get('aclIgmpType') != self.igmp_type_num)):
                            find_flag = False
                        if (tmp.get('aclLogFlag').lower() != str(self.log_flag).lower()):
                            find_flag = False
                        if find_flag:
                            break
                else:
                    find_flag = False
            if (self.state == 'present'):
                need_cfg = bool((not find_flag))
            elif (self.state == 'absent'):
                need_cfg = bool(find_flag)
            else:
                need_cfg = False
    self.cur_advance_rule_cfg['need_cfg'] = need_cfg