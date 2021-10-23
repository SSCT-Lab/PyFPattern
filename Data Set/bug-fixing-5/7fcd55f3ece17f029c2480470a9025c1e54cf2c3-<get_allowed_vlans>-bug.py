@classmethod
def get_allowed_vlans(cls, if_data):
    allowed_vlans = cls.get_config_attr(if_data, 'Allowed vlans')
    if allowed_vlans:
        vlans = allowed_vlans.split(',')
        allowed_vlans = [int(vlan.strip()) for vlan in vlans]
    return allowed_vlans