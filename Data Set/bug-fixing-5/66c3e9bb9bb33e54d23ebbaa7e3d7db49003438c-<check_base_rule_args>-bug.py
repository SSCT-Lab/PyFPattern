def check_base_rule_args(self):
    ' Check base rule invalid args '
    need_cfg = False
    find_flag = False
    self.cur_base_rule_cfg['base_rule_info'] = []
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
            if self.source_ip:
                if (not check_ip_addr(self.source_ip)):
                    self.module.fail_json(msg=('Error: The source_ip %s is invalid.' % self.source_ip))
                if (not self.src_mask):
                    self.module.fail_json(msg='Error: Please input src_mask.')
            if self.src_mask:
                if self.src_mask.isdigit():
                    if ((int(self.src_mask) < 1) or (int(self.src_mask) > 32)):
                        self.module.fail_json(msg='Error: The src_mask is out of [1 - 32].')
                    self.src_wild = self.get_wildcard_mask()
                else:
                    self.module.fail_json(msg='Error: The src_mask is not digit.')
            if self.vrf_name:
                if ((len(self.vrf_name) < 1) or (len(self.vrf_name) > 31)):
                    self.module.fail_json(msg='Error: The len of vrf_name is out of [1 - 31].')
            if self.time_range:
                if ((len(self.time_range) < 1) or (len(self.time_range) > 32)):
                    self.module.fail_json(msg='Error: The len of time_range is out of [1 - 32].')
            if self.rule_description:
                if ((len(self.rule_description) < 1) or (len(self.rule_description) > 127)):
                    self.module.fail_json(msg='Error: The len of rule_description is out of [1 - 127].')
                if ((self.state != 'delete_acl') and (not self.rule_id)):
                    self.module.fail_json(msg='Error: Please input rule_id.')
            conf_str = (CE_GET_ACL_BASE_RULE_HEADER % self.acl_name)
            if self.rule_id:
                conf_str += '<aclRuleID></aclRuleID>'
            if self.rule_action:
                conf_str += '<aclAction></aclAction>'
            if self.source_ip:
                conf_str += '<aclSourceIp></aclSourceIp>'
            if self.src_wild:
                conf_str += '<aclSrcWild></aclSrcWild>'
            if self.frag_type:
                conf_str += '<aclFragType></aclFragType>'
            if self.vrf_name:
                conf_str += '<vrfName></vrfName>'
            if self.time_range:
                conf_str += '<aclTimeName></aclTimeName>'
            if self.rule_description:
                conf_str += '<aclRuleDescription></aclRuleDescription>'
            conf_str += '<aclLogFlag></aclLogFlag>'
            conf_str += CE_GET_ACL_BASE_RULE_TAIL
            recv_xml = self.netconf_get_config(conf_str=conf_str)
            if ('<data/>' in recv_xml):
                find_flag = False
            else:
                xml_str = recv_xml.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
                root = ElementTree.fromstring(xml_str)
                base_rule_info = root.findall('acl/aclGroups/aclGroup/aclRuleBas4s/aclRuleBas4')
                if base_rule_info:
                    for tmp in base_rule_info:
                        tmp_dict = dict()
                        for site in tmp:
                            if (site.tag in ['aclRuleName', 'aclRuleID', 'aclAction', 'aclSourceIp', 'aclSrcWild', 'aclFragType', 'vrfName', 'aclTimeName', 'aclRuleDescription', 'aclLogFlag']):
                                tmp_dict[site.tag] = site.text
                        self.cur_base_rule_cfg['base_rule_info'].append(tmp_dict)
                if self.cur_base_rule_cfg['base_rule_info']:
                    for tmp in self.cur_base_rule_cfg['base_rule_info']:
                        find_flag = True
                        if (self.rule_name and (tmp.get('aclRuleName') != self.rule_name)):
                            find_flag = False
                        if (self.rule_id and (tmp.get('aclRuleID') != self.rule_id)):
                            find_flag = False
                        if (self.rule_action and (tmp.get('aclAction') != self.rule_action)):
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
                        if (self.frag_type and (tmp.get('aclFragType') != self.frag_type)):
                            find_flag = False
                        if (self.vrf_name and (tmp.get('vrfName') != self.vrf_name)):
                            find_flag = False
                        if (self.time_range and (tmp.get('aclTimeName') != self.time_range)):
                            find_flag = False
                        if (self.rule_description and (tmp.get('aclRuleDescription') != self.rule_description)):
                            find_flag = False
                        if (tmp.get('aclLogFlag') != str(self.log_flag).lower()):
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
    self.cur_base_rule_cfg['need_cfg'] = need_cfg