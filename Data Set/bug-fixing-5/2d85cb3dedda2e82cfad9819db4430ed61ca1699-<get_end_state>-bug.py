def get_end_state(self):
    'get end state info'
    if (self.info_center_enable or self.packet_priority or self.suppress_enable):
        self.cur_global_info = self.get_syslog_global()
    if (self.logfile_max_num or self.logfile_max_size):
        self.cur_logfile_info = self.get_syslog_logfile()
    if (self.channel_id and self.channel_cfg_name):
        self.channel_info = self.get_channel_dict()
    if (self.channel_out_direct and self.channel_id):
        self.channel_direct_info = self.get_channel_direct_dict()
    if (self.filter_feature_name and self.filter_log_name):
        self.filter_info = self.get_filter_dict()
    if self.ip_type:
        self.server_ip_info = self.get_server_ip_dict()
    if self.server_domain:
        self.server_domain_info = self.get_server_domain_dict()
    if self.info_center_enable:
        self.end_state['info_center_enable'] = self.cur_global_info['icEnable']
    if self.packet_priority:
        self.end_state['packet_priority'] = self.cur_global_info['packetPriority']
    if self.suppress_enable:
        self.end_state['suppress_enable'] = self.cur_global_info['suppressEnable']
    if self.logfile_max_num:
        self.end_state['logfile_max_num'] = self.cur_logfile_info['maxFileNum']
    if self.logfile_max_size:
        self.end_state['logfile_max_size'] = self.cur_logfile_info['maxFileSize']
    if (self.channel_id and self.channel_cfg_name):
        if self.channel_info:
            self.end_state['channel_id_info'] = self.channel_info['channelInfos']
    if (self.channel_out_direct and self.channel_id):
        if self.channel_direct_info:
            self.end_state['channel_out_direct_info'] = self.channel_direct_info['channelDirectInfos']
    if (self.filter_feature_name and self.filter_log_name):
        if self.filter_info:
            self.end_state['filter_id_info'] = self.filter_info['filterInfos']
    if self.ip_type:
        if self.server_ip_info:
            self.end_state['server_ip_info'] = self.server_ip_info['serverIpInfos']
    if self.server_domain:
        if self.server_domain_info:
            self.end_state['server_domain_info'] = self.server_domain_info['serverAddressInfos']