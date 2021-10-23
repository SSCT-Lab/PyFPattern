def get_exist_interface_statistic(self):
    'get exist netstream interface statistic parameter'
    statistic_tmp1 = dict()
    statistic_tmp1['statistics_direction'] = list()
    flags = list()
    exp = (' | ignore-case  section include ^#\\s+interface %s | include netstream inbound|outbound' % self.interface)
    flags.append(exp)
    config = get_config(self.module, flags)
    if (not config):
        statistic_tmp1['type'] = 'null'
    else:
        statistic_tmp1['type'] = 'ip'
        config = config.lstrip()
        config_list = config.split('\n')
        for config_mem in config_list:
            config_mem = config_mem.lstrip()
            config_mem_list = config_mem.split(' ')
            statistic_tmp1['statistics_direction'].append(str(config_mem_list[1]))
    statistic_tmp1['interface'] = self.interface
    self.existing['statistic'].append(statistic_tmp1)