def merge_syslog_global(self):
    'config global'
    conf_str = CE_NC_MERGE_CENTER_GLOBAL_INFO_HEADER
    if self.info_center_enable:
        conf_str += ('<icEnable>%s</icEnable>' % self.info_center_enable)
    if self.packet_priority:
        if (self.state == 'present'):
            packet_priority = self.packet_priority
        else:
            packet_priority = 0
        conf_str += ('<packetPriority>%s</packetPriority>' % packet_priority)
    if self.suppress_enable:
        conf_str += ('<suppressEnable>%s</suppressEnable>' % self.suppress_enable)
    conf_str += CE_NC_MERGE_CENTER_GLOBAL_INFO_TAIL
    if ((self.info_center_enable == 'true') and (self.cur_global_info['icEnable'] != self.info_center_enable)):
        cmd = 'info-center enable'
        self.updates_cmd.append(cmd)
        self.changed = True
    if ((self.suppress_enable == 'true') and (self.cur_global_info['suppressEnable'] != self.suppress_enable)):
        cmd = 'info-center statistic-suppress enable'
        self.updates_cmd.append(cmd)
        self.changed = True
    if ((self.info_center_enable == 'false') and (self.cur_global_info['icEnable'] != self.info_center_enable)):
        cmd = 'undo info-center enable'
        self.updates_cmd.append(cmd)
        self.changed = True
    if ((self.suppress_enable == 'false') and (self.cur_global_info['suppressEnable'] != self.suppress_enable)):
        cmd = 'undo info-center statistic-suppress enable'
        self.updates_cmd.append(cmd)
        self.changed = True
    if (self.state == 'present'):
        if self.packet_priority:
            if (self.cur_global_info['packetPriority'] != self.packet_priority):
                cmd = ('info-center syslog packet-priority %s' % self.packet_priority)
                self.updates_cmd.append(cmd)
                self.changed = True
    if (self.state == 'absent'):
        if self.packet_priority:
            if (self.cur_global_info['packetPriority'] == self.packet_priority):
                cmd = ('undo info-center syslog packet-priority %s' % self.packet_priority)
                self.updates_cmd.append(cmd)
                self.changed = True
    if self.changed:
        recv_xml = set_nc_config(self.module, conf_str)
        if ('<ok/>' not in recv_xml):
            self.module.fail_json(msg='Error: Merge syslog global failed.')