@classmethod
def get_access_vlan(cls, if_data):
    access_vlan = cls.get_config_attr(if_data, 'Access vlan')
    if access_vlan:
        return int(access_vlan)