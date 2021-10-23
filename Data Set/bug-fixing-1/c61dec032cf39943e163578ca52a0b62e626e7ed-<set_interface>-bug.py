

def set_interface(want, have):
    commands = []
    wants_access = want['access']
    if wants_access:
        access_vlan = wants_access.get('vlan')
        if (access_vlan and (access_vlan != have.get('access', {
            
        }).get('vlan'))):
            commands.append('switchport access vlan {0}'.format(access_vlan))
    wants_trunk = want['trunk']
    if wants_trunk:
        has_trunk = have.get('trunk', {
            
        })
        native_vlan = wants_trunk.get('native_vlan')
        if (native_vlan and (native_vlan != has_trunk.get('native_vlan'))):
            commands.append('switchport trunk native vlan {0}'.format(native_vlan))
        allowed_vlans = want['trunk'].get('trunk_allowed_vlans')
        has_allowed = has_trunk.get('trunk_allowed_vlans')
        if allowed_vlans:
            allowed_vlans = ','.join(allowed_vlans)
            commands.append('switchport trunk allowed vlan {0}'.format(allowed_vlans))
    if commands:
        commands.insert(0, 'interface {0}'.format(want['name']))
    return commands
