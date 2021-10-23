def get_end_sampler_interval(self):
    'get end netstream sampler interval'
    sampler_tmp = dict()
    sampler_tmp1 = dict()
    flags = list()
    exp = ' | ignore-case  include ^netstream sampler random-packets'
    flags.append(exp)
    config = get_config(self.module, flags)
    if (not config):
        sampler_tmp['sampler_interval'] = 'null'
        sampler_tmp['sampler_direction'] = 'null'
    else:
        config_list = config.split(' ')
        config_num = len(config_list)
        sampler_tmp['sampler_direction'] = config_list[(config_num - 1)]
        sampler_tmp['sampler_interval'] = config_list[(config_num - 2)]
    sampler_tmp['interface'] = 'all'
    self.end_state['sampler'].append(sampler_tmp)
    if (self.interface != 'all'):
        flags = list()
        exp = (' | ignore-case  section include ^#\\s+interface %s | include netstream sampler random-packets' % self.interface)
        flags.append(exp)
        config = get_config(self.module, flags)
        if (not config):
            sampler_tmp1['sampler_interval'] = 'null'
            sampler_tmp1['sampler_direction'] = 'null'
        else:
            config = config.lstrip()
            config_list = config.split('\n')
            for config_mem in config_list:
                sampler_tmp1 = dict()
                config_mem_list = config_mem.split(' ')
                config_num = len(config_mem_list)
                sampler_tmp1['sampler_direction'] = config_mem_list[(config_num - 1)]
                sampler_tmp1['sampler_interval'] = config_mem_list[(config_num - 2)]
                sampler_tmp1['interface'] = self.interface
                self.end_state['sampler'].append(sampler_tmp1)