def main():
    argument_spec = dict(vrf=dict(required=True), afi=dict(required=True, choices=['ipv4', 'ipv6']), route_target_both_auto_evpn=dict(required=False, type='bool'), state=dict(choices=['present', 'absent'], default='present'), m_facts=dict(default=False, type='bool', removed_in_version='2.4'), safi=dict(choices=['unicast', 'multicast'], removed_in_version='2.4'))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    result = {
        'changed': False,
        'warnings': warnings,
    }
    config_text = get_config(module)
    config = NetworkConfig(indent=2, contents=config_text)
    path = [('vrf context %s' % module.params['vrf']), ('address-family %s unicast' % module.params['afi'])]
    try:
        current = config.get_block_config(path)
    except ValueError:
        current = None
    commands = list()
    if (current and (module.params['state'] == 'absent')):
        commands.append(('no address-family %s unicast' % module.params['afi']))
    elif (module.params['state'] == 'present'):
        if current:
            have = ('route-target both auto evpn' in current)
            want = bool(module.params['route_target_both_auto_evpn'])
            if (want and (not have)):
                commands.append(('address-family %s unicast' % module.params['afi']))
                commands.append('route-target both auto evpn')
            elif (have and (not want)):
                commands.append(('address-family %s unicast' % module.params['afi']))
                commands.append('no route-target both auto evpn')
        else:
            commands.append(('address-family %s unicast' % module.params['afi']))
            if module.params['route_target_both_auto_evpn']:
                commands.append('route-target both auto evpn')
    if commands:
        commands.insert(0, ('vrf context %s' % module.params['vrf']))
        if (not module.check_mode):
            load_config(module, commands)
        result['changed'] = True
    result['commands'] = commands
    module.exit_json(**result)