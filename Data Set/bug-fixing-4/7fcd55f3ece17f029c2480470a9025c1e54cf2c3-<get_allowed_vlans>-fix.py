@classmethod
def get_allowed_vlans(cls, if_data):
    allowed_vlans = cls.get_config_attr(if_data, 'Allowed vlans')
    interface_allwoed_vlans = []
    if allowed_vlans:
        vlans = [x.strip() for x in allowed_vlans.split(',')]
        for vlan in vlans:
            if ('-' not in vlan):
                interface_allwoed_vlans.append(int(vlan))
            else:
                vlan_range = vlan.split('-')
                min_number = int(vlan_range[0].strip())
                max_number = int(vlan_range[1].strip())
                vlan_list = range(min_number, (max_number + 1))
                interface_allwoed_vlans.extend(vlan_list)
    return interface_allwoed_vlans