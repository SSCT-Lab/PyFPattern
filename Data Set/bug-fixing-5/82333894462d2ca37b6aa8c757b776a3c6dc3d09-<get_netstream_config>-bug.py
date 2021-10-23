def get_netstream_config(self):
    'get current netstream configuration'
    flags = list()
    exp = ' | inc ^netstream export'
    flags.append(exp)
    return get_config(self.module, flags)