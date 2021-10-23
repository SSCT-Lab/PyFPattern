def get_end_statistic_record(self):
    'get end netstream statistic record parameter'
    if (self.statistics_record and self.statistics_direction):
        self.module.fail_json(msg='Error: The statistic direction and record can not exist at the same time.')
    statistic_tmp = dict()
    statistic_tmp1 = dict()
    statistic_tmp['statistics_record'] = list()
    statistic_tmp['interface'] = self.interface
    statistic_tmp1['statistics_record'] = list()
    statistic_tmp1['interface'] = self.interface
    flags = list()
    exp = (' | ignore-case  section include ^#\\s+interface %s | include netstream record' % self.interface)
    flags.append(exp)
    config = get_config(self.module, flags)
    if (not config):
        statistic_tmp['type'] = 'ip'
        self.end_state['flexible_statistic'].append(statistic_tmp)
        statistic_tmp1['type'] = 'vxlan'
        self.end_state['flexible_statistic'].append(statistic_tmp1)
    else:
        config = config.lstrip()
        config_list = config.split('\n')
        for config_mem in config_list:
            config_mem = config_mem.lstrip()
            statistic_tmp['statistics_record'] = list()
            config_mem_list = config_mem.split(' ')
            if (str(config_mem_list[3]) == 'ip'):
                statistic_tmp['statistics_record'].append(str(config_mem_list[2]))
        statistic_tmp['type'] = 'ip'
        self.end_state['flexible_statistic'].append(statistic_tmp)
        for config_mem in config_list:
            statistic_tmp1['statistics_record'] = list()
            config_mem = config_mem.lstrip()
            config_mem_list = config_mem.split(' ')
            if (str(config_mem_list[3]) == 'vxlan'):
                statistic_tmp1['statistics_record'].append(str(config_mem_list[2]))
        statistic_tmp1['type'] = 'vxlan'
        self.end_state['flexible_statistic'].append(statistic_tmp1)