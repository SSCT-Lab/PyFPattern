def main():
    'Module main'
    argument_spec = dict(interface=dict(required=True, type='str'), mode=dict(choices=['access', 'trunk', 'dot1qtunnel', 'hybrid'], required=False), default_vlan=dict(type='str', required=False), pvid_vlan=dict(type='str', required=False), trunk_vlans=dict(type='str', required=False), untagged_vlans=dict(type='str', required=False), tagged_vlans=dict(type='str', required=False), state=dict(choices=['absent', 'present', 'unconfigured'], default='present'))
    argument_spec.update(ce_argument_spec)
    switchport = SwitchPort(argument_spec)
    switchport.work()