def delete_adv_rule(self):
    ' Delete advance rule operation '
    conf_str = (CE_DELETE_ACL_ADVANCE_RULE_HEADER % (self.acl_name, self.rule_name))
    if self.rule_id:
        conf_str += ('<aclRuleID>%s</aclRuleID>' % self.rule_id)
    if self.rule_action:
        conf_str += ('<aclAction>%s</aclAction>' % self.rule_action)
    if self.protocol:
        conf_str += ('<aclProtocol>%s</aclProtocol>' % self.protocol_num)
    if self.source_ip:
        conf_str += ('<aclSourceIp>%s</aclSourceIp>' % self.source_ip)
    if self.src_wild:
        conf_str += ('<aclSrcWild>%s</aclSrcWild>' % self.src_wild)
    if self.src_pool_name:
        conf_str += ('<aclSPoolName>%s</aclSPoolName>' % self.src_pool_name)
    if self.dest_ip:
        conf_str += ('<aclDestIp>%s</aclDestIp>' % self.dest_ip)
    if self.dest_wild:
        conf_str += ('<aclDestWild>%s</aclDestWild>' % self.dest_wild)
    if self.dest_pool_name:
        conf_str += ('<aclDPoolName>%s</aclDPoolName>' % self.dest_pool_name)
    if self.src_port_op:
        conf_str += ('<aclSrcPortOp>%s</aclSrcPortOp>' % self.src_port_op)
    if self.src_port_begin:
        conf_str += ('<aclSrcPortBegin>%s</aclSrcPortBegin>' % self.src_port_begin)
    if self.src_port_end:
        conf_str += ('<aclSrcPortEnd>%s</aclSrcPortEnd>' % self.src_port_end)
    if self.src_port_pool_name:
        conf_str += ('<aclSPortPoolName>%s</aclSPortPoolName>' % self.src_port_pool_name)
    if self.dest_port_op:
        conf_str += ('<aclDestPortOp>%s</aclDestPortOp>' % self.dest_port_op)
    if self.dest_port_begin:
        conf_str += ('<aclDestPortB>%s</aclDestPortB>' % self.dest_port_begin)
    if self.dest_port_end:
        conf_str += ('<aclDestPortE>%s</aclDestPortE>' % self.dest_port_end)
    if self.dest_port_pool_name:
        conf_str += ('<aclDPortPoolName>%s</aclDPortPoolName>' % self.dest_port_pool_name)
    if self.frag_type:
        conf_str += ('<aclFragType>%s</aclFragType>' % self.frag_type)
    if self.precedence:
        conf_str += ('<aclPrecedence>%s</aclPrecedence>' % self.precedence)
    if self.tos:
        conf_str += ('<aclTos>%s</aclTos>' % self.tos)
    if self.dscp:
        conf_str += ('<aclDscp>%s</aclDscp>' % self.dscp)
    if self.icmp_name:
        conf_str += ('<aclIcmpName>%s</aclIcmpName>' % self.icmp_name)
    if self.icmp_type:
        conf_str += ('<aclIcmpType>%s</aclIcmpType>' % self.icmp_type)
    if self.icmp_code:
        conf_str += ('<aclIcmpCode>%s</aclIcmpCode>' % self.icmp_code)
    conf_str += ('<aclTtlExpired>%s</aclTtlExpired>' % str(self.ttl_expired).lower())
    if self.vrf_name:
        conf_str += ('<vrfName>%s</vrfName>' % self.vrf_name)
    if self.syn_flag:
        conf_str += ('<aclSynFlag>%s</aclSynFlag>' % self.syn_flag)
    if self.tcp_flag_mask:
        conf_str += ('<aclTcpFlagMask>%s</aclTcpFlagMask>' % self.tcp_flag_mask)
    if (self.protocol == 'tcp'):
        conf_str += ('<aclEstablished>%s</aclEstablished>' % str(self.established).lower())
    if self.time_range:
        conf_str += ('<aclTimeName>%s</aclTimeName>' % self.time_range)
    if self.rule_description:
        conf_str += ('<aclRuleDescription>%s</aclRuleDescription>' % self.rule_description)
    if self.igmp_type:
        conf_str += ('<aclIgmpType>%s</aclIgmpType>' % self.igmp_type)
    conf_str += ('<aclLogFlag>%s</aclLogFlag>' % str(self.log_flag).lower())
    conf_str += CE_DELETE_ACL_ADVANCE_RULE_TAIL
    recv_xml = self.netconf_set_config(conf_str=conf_str)
    if ('<ok/>' not in recv_xml):
        self.module.fail_json(msg='Error: Delete acl base rule failed.')
    if self.rule_description:
        if self.acl_name.isdigit():
            cmd = ('acl number %s' % self.acl_name)
        else:
            cmd = ('acl name %s' % self.acl_name)
        self.updates_cmd.append(cmd)
        cmd = ('undo rule %s description' % self.rule_id)
        self.updates_cmd.append(cmd)
    if self.rule_id:
        if self.acl_name.isdigit():
            cmd = ('acl number %s' % self.acl_name)
        else:
            cmd = ('acl name %s' % self.acl_name)
        self.updates_cmd.append(cmd)
        cmd = ('undo rule %s' % self.rule_id)
        self.updates_cmd.append(cmd)
    elif (self.rule_action and self.protocol):
        if self.acl_name.isdigit():
            cmd = ('acl number %s' % self.acl_name)
        else:
            cmd = ('acl name %s' % self.acl_name)
        self.updates_cmd.append(cmd)
        cmd = 'undo rule'
        cmd += (' %s' % self.rule_action)
        cmd += (' %s' % self.protocol)
        if self.dscp:
            cmd += (' dscp %s' % self.dscp)
        if self.tos:
            cmd += (' tos %s' % self.tos)
        if (self.source_ip and self.src_mask):
            cmd += (' source %s %s' % (self.source_ip, self.src_mask))
        if self.src_pool_name:
            cmd += (' source-pool %s' % self.src_pool_name)
        if self.src_port_op:
            cmd += ' source-port'
            if (self.src_port_op == 'lt'):
                cmd += (' lt %s' % self.src_port_end)
            elif (self.src_port_op == 'eq'):
                cmd += (' eq %s' % self.src_port_begin)
            elif (self.src_port_op == 'gt'):
                cmd += (' gt %s' % self.src_port_begin)
            elif (self.src_port_op == 'range'):
                cmd += (' range %s %s' % (self.src_port_begin, self.src_port_end))
        if self.src_port_pool_name:
            cmd += (' source-port-pool %s' % self.src_port_pool_name)
        if (self.dest_ip and self.dest_mask):
            cmd += (' destination %s %s' % (self.dest_ip, self.dest_mask))
        if self.dest_pool_name:
            cmd += (' destination-pool %s' % self.dest_pool_name)
        if self.dest_port_op:
            cmd += ' destination-port'
            if (self.dest_port_op == 'lt'):
                cmd += (' lt %s' % self.dest_port_end)
            elif (self.dest_port_op == 'eq'):
                cmd += (' eq %s' % self.dest_port_begin)
            elif (self.dest_port_op == 'gt'):
                cmd += (' gt %s' % self.dest_port_begin)
            elif (self.dest_port_op == 'range'):
                cmd += (' range %s %s' % (self.dest_port_begin, self.dest_port_end))
        if self.dest_port_pool_name:
            cmd += (' destination-port-pool %s' % self.dest_port_pool_name)
        if (self.frag_type == 'fragment'):
            cmd += ' fragment-type fragment'
        if self.precedence:
            cmd += (' precedence %s' % self.precedence_name[self.precedence])
        if self.time_range:
            cmd += (' time-range %s' % self.time_range)
        if self.vrf_name:
            cmd += (' vpn-instance %s' % self.vrf_name)
        if self.ttl_expired:
            cmd += ' ttl-expired'
        if self.log_flag:
            cmd += ' logging'
        self.updates_cmd.append(cmd)
    self.changed = True