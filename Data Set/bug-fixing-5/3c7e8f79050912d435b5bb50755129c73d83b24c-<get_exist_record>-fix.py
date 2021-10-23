def get_exist_record(self):
    'get exist netstream record'
    flags = list()
    exp = ' | ignore-case include netstream record'
    flags.append(exp)
    config = get_config(self.module, flags)
    if config:
        config = config.lstrip()
        config_list = config.split('\n')
        for config_mem in config_list:
            config_mem_list = config_mem.split(' ')
            if (config_mem_list[3] == 'ip'):
                self.existing['ip_record'].append(config_mem_list[2])
            if (config_mem_list[3] == 'vxlan'):
                self.existing['vxlan_record'].append(config_mem_list[2])