def get_list_of_vlans(module):
    body = run_commands(module, ['show vlan | json'])[0]
    vlan_list = []
    vlan_table = body.get('TABLE_vlanbrief')['ROW_vlanbrief']
    if isinstance(vlan_table, list):
        for vlan in vlan_table:
            vlan_list.append(str(vlan['vlanshowbr-vlanid-utf']))
    else:
        vlan_list.append('1')
    return vlan_list