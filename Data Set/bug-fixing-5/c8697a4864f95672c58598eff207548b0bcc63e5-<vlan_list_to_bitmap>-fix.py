def vlan_list_to_bitmap(self, vlanlist):
    ' convert vlan list to vlan bitmap '
    vlan_bit = (['0'] * 1024)
    bit_int = ([0] * 1024)
    vlan_list_len = len(vlanlist)
    for num in range(vlan_list_len):
        tagged_vlans = int(vlanlist[num])
        if ((tagged_vlans <= 0) or (tagged_vlans > 4094)):
            self.module.fail_json(msg='Error: Vlan id is not in the range from 1 to 4094.')
        j = (tagged_vlans // 4)
        bit_int[j] |= (8 >> (tagged_vlans % 4))
        vlan_bit[j] = hex(bit_int[j])[2]
    vlan_xml = ''.join(vlan_bit)
    return vlan_xml