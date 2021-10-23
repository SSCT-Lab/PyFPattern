def main():
    'Module main'
    argument_spec = dict(interface=dict(required=True, type='str'), mode=dict(choices=['access', 'trunk'], required=False), access_vlan=dict(type='str', required=False), native_vlan=dict(type='str', required=False), trunk_vlans=dict(type='str', required=False), state=dict(choices=['absent', 'present', 'unconfigured'], default='present'))
    argument_spec.update(ce_argument_spec)
    switchport = SwitchPort(argument_spec)
    switchport.work()