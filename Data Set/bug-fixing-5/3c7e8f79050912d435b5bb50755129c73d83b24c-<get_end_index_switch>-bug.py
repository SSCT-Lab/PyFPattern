def get_end_index_switch(self):
    'get end netstream index switch'
    index_switch_tmp = dict()
    index_switch_tmp1 = dict()
    index_switch_tmp['index-switch'] = '16'
    index_switch_tmp['type'] = 'ip'
    index_switch_tmp1['index-switch'] = '16'
    index_switch_tmp1['type'] = 'vxlan'
    flags = list()
    exp = ' | ignore-case  include index-switch'
    flags.append(exp)
    config = get_config(self.module, flags)
    if (not config):
        self.end_state['index-switch'].append(index_switch_tmp)
        self.end_state['index-switch'].append(index_switch_tmp1)
    else:
        config = config.lstrip()
        config_list = config.split('\n')
        for config_mem in config_list:
            config_mem_list = config_mem.split(' ')
            if (str(config_mem_list[2]) == 'ip'):
                index_switch_tmp['index-switch'] = '32'
                index_switch_tmp['type'] = 'ip'
            if (str(config_mem_list[2]) == 'vxlan'):
                index_switch_tmp1['index-switch'] = '32'
                index_switch_tmp1['type'] = 'vxlan'
        self.end_state['index-switch'].append(index_switch_tmp)
        self.end_state['index-switch'].append(index_switch_tmp1)