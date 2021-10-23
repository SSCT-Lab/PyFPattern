def get_exist_timer_out_para(self):
    'Get exist netstream timeout parameters'
    active_tmp = dict()
    inactive_tmp = dict()
    tcp_tmp = dict()
    active_tmp['ip'] = '30'
    active_tmp['vxlan'] = '30'
    inactive_tmp['ip'] = '30'
    inactive_tmp['vxlan'] = '30'
    tcp_tmp['ip'] = 'absent'
    tcp_tmp['vxlan'] = 'absent'
    cmd = 'display current-configuration | include ^netstream timeout'
    (rc, out, err) = exec_command(self.module, cmd)
    if (rc != 0):
        self.module.fail_json(msg=err)
    config = str(out).strip()
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
    self.existing['active_timeout'].append(active_tmp)
    self.existing['inactive_timeout'].append(inactive_tmp)
    self.existing['tcp_timeout'].append(tcp_tmp)