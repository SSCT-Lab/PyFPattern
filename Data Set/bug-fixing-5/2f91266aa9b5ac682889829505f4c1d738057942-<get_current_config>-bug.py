def get_current_config(self):
    'get current configuration'
    flags = list()
    exp = ' | ignore-case section include dfs-group'
    if self.vpn_instance:
        exp += ('|^ip vpn-instance %s$' % self.vpn_instance)
    if self.vbdif_name:
        exp += ('|^interface %s$' % self.vbdif_name)
    flags.append(exp)
    return self.get_config(flags)