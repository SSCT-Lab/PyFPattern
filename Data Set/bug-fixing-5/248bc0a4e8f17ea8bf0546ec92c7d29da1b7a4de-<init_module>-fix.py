def init_module(self):
    '\n        init ansible NetworkModule.\n        '
    required_one_of = [['vlan_id', 'vlan_range']]
    mutually_exclusive = [['vlan_id', 'vlan_range']]
    self.module = AnsibleModule(argument_spec=self.spec, required_one_of=required_one_of, mutually_exclusive=mutually_exclusive, supports_check_mode=True)