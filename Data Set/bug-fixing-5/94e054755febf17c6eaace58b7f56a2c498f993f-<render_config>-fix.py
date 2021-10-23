def render_config(self, spec, conf):
    '\n        Render config as dictionary structure and delete keys\n          from spec for null values\n        :param spec: The facts tree, generated from the argspec\n        :param conf: The configuration\n        :rtype: dictionary\n        :returns: The generated config\n        '
    config = deepcopy(spec)
    match = re.search('^(\\S+)', conf)
    intf = match.group(1)
    if (get_interface_type(intf) == 'unknown'):
        return {
            
        }
    config['name'] = intf
    ipv4_match = re.compile('\\n  ip address (.*)')
    matches = ipv4_match.findall(conf)
    if matches:
        if matches[0]:
            config['ipv4'] = []
            for m in matches:
                ipv4_conf = m.split()
                addr = ipv4_conf[0]
                if addr:
                    config_dict = {
                        'address': addr,
                    }
                    if (len(ipv4_conf) > 1):
                        d = ipv4_conf[1]
                        if (d == 'secondary'):
                            config_dict.update({
                                'secondary': True,
                            })
                            if (len(ipv4_conf) == 4):
                                if (ipv4_conf[2] == 'tag'):
                                    config_dict.update({
                                        'tag': int(ipv4_conf[(- 1)]),
                                    })
                        elif (d == 'tag'):
                            config_dict.update({
                                'tag': int(ipv4_conf[(- 1)]),
                            })
                    config['ipv4'].append(config_dict)
    ipv6_match = re.compile('\\n  ipv6 address (.*)')
    matches = ipv6_match.findall(conf)
    if matches:
        if matches[0]:
            config['ipv6'] = []
            for m in matches:
                ipv6_conf = m.split()
                addr = ipv6_conf[0]
                if addr:
                    config_dict = {
                        'address': addr,
                    }
                    if (len(ipv6_conf) > 1):
                        d = ipv6_conf[1]
                        if (d == 'tag'):
                            config_dict.update({
                                'tag': int(ipv6_conf[(- 1)]),
                            })
                    config['ipv6'].append(config_dict)
    return utils.remove_empties(config)