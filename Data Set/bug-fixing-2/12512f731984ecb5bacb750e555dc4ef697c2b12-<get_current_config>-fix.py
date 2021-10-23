

def get_current_config(self):
    'get current configuration'
    flags = list()
    exp = '| ignore-case section include evn bgp|host collect protocol bgp'
    if self.vbdif_name:
        exp += ('|^#\\s+interface %s\\s+' % self.vbdif_name.lower().capitalize().replace(' ', ''))
    if self.bridge_domain_id:
        exp += ('|^#\\s+bridge-domain %s\\s+' % self.bridge_domain_id)
    flags.append(exp)
    cfg_str = self.get_config(flags)
    config = cfg_str.split('\n')
    exist_config = ''
    for cfg in config:
        if (not cfg.startswith('display')):
            exist_config += cfg
    return exist_config
