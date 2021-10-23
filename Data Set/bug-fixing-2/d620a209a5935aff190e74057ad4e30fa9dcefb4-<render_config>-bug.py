

def render_config(self, spec, conf):
    '\n        Render config as dictionary structure and delete keys from spec for null values\n        :param spec: The facts tree, generated from the argspec\n        :param conf: The configuration\n        :rtype: dictionary\n        :returns: The generated config\n        '
    config = deepcopy(spec)
    match = re.search('^(\\S+)', conf)
    intf = match.group(1)
    if (get_interface_type(intf) == 'unknown'):
        return {
            
        }
    if intf.lower().startswith('gi'):
        config['name'] = normalize_interface(intf)
        has_access = utils.parse_conf_arg(conf, 'switchport access vlan')
        if has_access:
            config['access'] = {
                'vlan': int(has_access),
            }
        trunk = dict()
        trunk['encapsulation'] = utils.parse_conf_arg(conf, 'encapsulation')
        native_vlan = utils.parse_conf_arg(conf, 'native vlan')
        if native_vlan:
            trunk['native_vlan'] = int(native_vlan)
        allowed_vlan = utils.parse_conf_arg(conf, 'allowed vlan')
        if allowed_vlan:
            trunk['allowed_vlans'] = allowed_vlan.split(',')
        pruning_vlan = utils.parse_conf_arg(conf, 'pruning vlan')
        if pruning_vlan:
            trunk['pruning_vlans'] = pruning_vlan.split(',')
        config['trunk'] = trunk
    return utils.remove_empties(config)
