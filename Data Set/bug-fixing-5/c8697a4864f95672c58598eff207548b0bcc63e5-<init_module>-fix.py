def init_module(self):
    ' init module '
    required_if = [('state', 'absent', ['mode']), ('state', 'present', ['mode'])]
    mutually_exclusive = [['default_vlan', 'trunk_vlans'], ['default_vlan', 'pvid_vlan'], ['default_vlan', 'untagged_vlans'], ['trunk_vlans', 'untagged_vlans'], ['trunk_vlans', 'tagged_vlans'], ['default_vlan', 'tagged_vlans']]
    self.module = AnsibleModule(argument_spec=self.spec, required_if=required_if, supports_check_mode=True, mutually_exclusive=mutually_exclusive)