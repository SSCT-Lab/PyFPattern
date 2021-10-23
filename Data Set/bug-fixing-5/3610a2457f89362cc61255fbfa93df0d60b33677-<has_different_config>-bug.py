def has_different_config(self, net):
    '\n        Evaluates an existing network and returns a tuple containing a boolean\n        indicating if the configuration is different and a list of differences.\n\n        :param net: the inspection output for an existing network\n        :return: (bool, list)\n        '
    different = False
    differences = []
    if (self.parameters.driver and (self.parameters.driver != net['Driver'])):
        different = True
        differences.append('driver')
    if self.parameters.driver_options:
        if (not net.get('Options')):
            different = True
            differences.append('driver_options')
        else:
            for (key, value) in self.parameters.driver_options.items():
                if ((not net['Options'].get(key)) or (value != net['Options'][key])):
                    different = True
                    differences.append(('driver_options.%s' % key))
    if self.parameters.ipam_driver:
        if ((not net.get('IPAM')) or (net['IPAM']['Driver'] != self.parameters.ipam_driver)):
            different = True
            differences.append('ipam_driver')
    if self.parameters.ipam_options:
        if ((not net.get('IPAM')) or (not net['IPAM'].get('Config'))):
            different = True
            differences.append('ipam_options')
        else:
            for (key, value) in self.parameters.ipam_options.items():
                camelkey = None
                for net_key in net['IPAM']['Config'][0]:
                    if (key == net_key.lower()):
                        camelkey = net_key
                        break
                if (not camelkey):
                    different = True
                    differences.append(('ipam_options.%s' % key))
                elif (net['IPAM']['Config'][0].get(camelkey) != value):
                    different = True
                    differences.append(('ipam_options.%s' % key))
    return (different, differences)