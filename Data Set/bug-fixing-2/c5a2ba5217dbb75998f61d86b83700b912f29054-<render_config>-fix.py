

def render_config(self, spec, conf, vlan_info):
    '\n        Render config as dictionary structure and delete keys\n          from spec for null values\n\n        :param spec: The facts tree, generated from the argspec\n        :param conf: The configuration\n        :rtype: dictionary\n        :returns: The generated config\n        '
    config = deepcopy(spec)
    if ((vlan_info == 'Name') and ('Name' not in conf)):
        conf = list(filter(None, conf.split(' ')))
        config['vlan_id'] = int(conf[0])
        config['name'] = conf[1]
        if (len(conf[2].split('/')) > 1):
            if (conf[2].split('/')[0] == 'sus'):
                config['state'] = 'suspend'
            elif (conf[2].split('/')[0] == 'act'):
                config['state'] = 'active'
            config['shutdown'] = 'enabled'
        else:
            if (conf[2] == 'suspended'):
                config['state'] = 'suspend'
            elif (conf[2] == 'active'):
                config['state'] = 'active'
            config['shutdown'] = 'disabled'
    elif ((vlan_info == 'Type') and ('Type' not in conf)):
        conf = list(filter(None, conf.split(' ')))
        config['mtu'] = int(conf[3])
    elif (vlan_info == 'Remote'):
        if ((len(conf.split(',')) > 1) or conf.isdigit()):
            remote_span_vlan = []
            if (len(conf.split(',')) > 1):
                remote_span_vlan = conf.split(',')
            else:
                remote_span_vlan.append(conf)
            remote_span = []
            for each in remote_span_vlan:
                remote_span.append(int(each))
            config['remote_span'] = remote_span
    return utils.remove_empties(config)
