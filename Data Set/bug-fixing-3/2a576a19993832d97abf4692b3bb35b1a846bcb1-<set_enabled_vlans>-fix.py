def set_enabled_vlans(api, name, vlans_enabled_list):
    updated = False
    to_add_vlans = []
    try:
        if (vlans_enabled_list is None):
            return updated
        vlans_enabled_list = list(vlans_enabled_list)
        current_vlans = get_vlan(api, name)
        if ('ALL' in vlans_enabled_list):
            if ((len(current_vlans['vlans']) > 0) or (current_vlans['state'] is 'STATE_ENABLED')):
                api.LocalLB.VirtualServer.set_vlan(virtual_servers=[name], vlans=[{
                    'state': 'STATE_DISABLED',
                    'vlans': [],
                }])
                updated = True
        else:
            if (current_vlans['state'] is 'STATE_DISABLED'):
                to_add_vlans = vlans_enabled_list
            else:
                for vlan in vlans_enabled_list:
                    if (vlan not in current_vlans['vlans']):
                        updated = True
                        to_add_vlans = vlans_enabled_list
                        break
            if updated:
                api.LocalLB.VirtualServer.set_vlan(virtual_servers=[name], vlans=[{
                    'state': 'STATE_ENABLED',
                    'vlans': [to_add_vlans],
                }])
        return updated
    except bigsuds.OperationFailed as e:
        raise Exception(('Error on setting enabled vlans : %s' % e))