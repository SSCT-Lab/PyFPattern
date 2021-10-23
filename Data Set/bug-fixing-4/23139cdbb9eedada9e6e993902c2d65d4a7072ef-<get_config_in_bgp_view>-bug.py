def get_config_in_bgp_view(self):
    'Get configuration in BGP view'
    flags = list()
    exp = ' | section include'
    if self.as_number:
        if self.bgp_instance:
            exp += (' bgp %s instance %s' % (self.as_number, self.bgp_instance))
        else:
            exp += (' bgp %s' % self.as_number)
    flags.append(exp)
    config = get_config(self.module, flags)
    return config