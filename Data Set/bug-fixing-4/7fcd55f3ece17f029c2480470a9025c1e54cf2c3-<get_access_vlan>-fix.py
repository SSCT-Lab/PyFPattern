@classmethod
def get_access_vlan(cls, if_data):
    access_vlan = cls.get_config_attr(if_data, 'Access vlan')
    if access_vlan:
        try:
            return int(access_vlan)
        except ValueError:
            return None