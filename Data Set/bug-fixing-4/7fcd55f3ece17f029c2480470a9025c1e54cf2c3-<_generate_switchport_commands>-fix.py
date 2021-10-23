def _generate_switchport_commands(self, if_name, req_conf):
    commands = []
    curr_conf = self._current_config.get(if_name, {
        
    })
    curr_mode = curr_conf.get('mode')
    req_mode = req_conf.get('mode')
    if (req_mode != curr_mode):
        commands.append(('switchport mode %s' % req_mode))
    curr_access_vlan = curr_conf.get('access_vlan')
    req_access_vlan = req_conf.get('access_vlan')
    if ((curr_access_vlan != req_access_vlan) and req_access_vlan):
        commands.append(('switchport access vlan %s' % req_access_vlan))
    curr_trunk_vlans = (curr_conf.get('trunk_allowed_vlans') or set())
    if curr_trunk_vlans:
        curr_trunk_vlans = set(curr_trunk_vlans)
    req_trunk_vlans = (req_conf.get('trunk_allowed_vlans') or set())
    if req_trunk_vlans:
        req_trunk_vlans = set(req_trunk_vlans)
    if ((req_mode != 'access') and (curr_trunk_vlans != req_trunk_vlans)):
        added_vlans = (req_trunk_vlans - curr_trunk_vlans)
        for vlan_id in added_vlans:
            commands.append(('switchport %s allowed-vlan add %s' % (req_mode, vlan_id)))
        removed_vlans = (curr_trunk_vlans - req_trunk_vlans)
        for vlan_id in removed_vlans:
            commands.append(('switchport %s allowed-vlan remove %s' % (req_mode, vlan_id)))
    if commands:
        self._add_interface_commands(if_name, commands)