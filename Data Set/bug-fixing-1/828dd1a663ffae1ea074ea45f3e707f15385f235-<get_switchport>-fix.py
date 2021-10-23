

def get_switchport(name, module):
    config = run_commands(module, ['show interface {0} switchport'.format(name)])[0]
    mode = re.search('Administrative Mode: (?:.* )?(\\w+)$', config, re.M)
    access = re.search('Access Mode VLAN: (\\d+)', config)
    native = re.search('Trunking Native Mode VLAN: (\\d+)', config)
    trunk = re.search('Trunking VLANs Enabled: (.+)$', config, re.M)
    if mode:
        mode = mode.group(1)
    if access:
        access = access.group(1)
    if native:
        native = native.group(1)
    if trunk:
        trunk = trunk.group(1)
    if (trunk == 'ALL'):
        trunk = '1-4094'
    switchport_config = {
        'interface': name,
        'mode': mode,
        'access_vlan': access,
        'native_vlan': native,
        'trunk_vlans': trunk,
    }
    return switchport_config
