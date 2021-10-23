def get_current_config(self):
    'get current configuration'
    flags = list()
    exp = ('| ignore-case section include bgp %s' % self.bgp_instance)
    flags.append(exp)
    return get_config(self.module, flags)