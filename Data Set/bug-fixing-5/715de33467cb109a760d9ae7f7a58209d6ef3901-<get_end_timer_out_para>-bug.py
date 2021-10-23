def get_end_timer_out_para(self):
    'Get end netstream timeout parameters'
    active_tmp = dict()
    inactive_tmp = dict()
    tcp_tmp = dict()
    active_tmp['ip'] = '30'
    active_tmp['vxlan'] = '30'
    inactive_tmp['ip'] = '30'
    inactive_tmp['vxlan'] = '30'
    tcp_tmp['ip'] = 'absent'
    tcp_tmp['vxlan'] = 'absent'
    flags = list()
    exp = ' | ignore-case include netstream timeout'
    exp = '| ignore-case include evpn-overlay enable'
    flags.append(exp)
    config = get_config(self.module, flags)
    if config:
        config = config.lstrip()
        config_list = config.split('\n')
        for config_mem in config_list:
            config_mem = config_mem.lstrip()
            config_mem_list = config_mem.split(' ')
            if (config_mem_list[2] == 'ip'):
                if (config_mem_list[3] == 'active'):
                    active_tmp['ip'] = config_mem_list[4]
                if (config_mem_list[3] == 'inactive'):
                    inactive_tmp['ip'] = config_mem_list[4]
                if (config_mem_list[3] == 'tcp-session'):
                    tcp_tmp['ip'] = 'present'
            if (config_mem_list[2] == 'vxlan'):
                if (config_mem_list[4] == 'active'):
                    active_tmp['vxlan'] = config_mem_list[5]
                if (config_mem_list[4] == 'inactive'):
                    inactive_tmp['vxlan'] = config_mem_list[5]
                if (config_mem_list[4] == 'tcp-session'):
                    tcp_tmp['vxlan'] = 'present'
    self.end_state['active_timeout'].append(active_tmp)
    self.end_state['inactive_timeout'].append(inactive_tmp)
    self.end_state['tcp_timeout'].append(tcp_tmp)