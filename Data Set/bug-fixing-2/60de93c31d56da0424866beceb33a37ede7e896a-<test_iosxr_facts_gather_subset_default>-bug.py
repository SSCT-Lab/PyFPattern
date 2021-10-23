

def test_iosxr_facts_gather_subset_default(self):
    set_module_args(dict())
    result = self.execute_module()
    ansible_facts = result['ansible_facts']
    self.assertIn('hardware', ansible_facts['ansible_net_gather_subset'])
    self.assertIn('default', ansible_facts['ansible_net_gather_subset'])
    self.assertIn('interfaces', ansible_facts['ansible_net_gather_subset'])
    self.assertEquals('iosxr01', ansible_facts['ansible_net_hostname'])
    self.assertEquals(['disk0:', 'flash0:'], ansible_facts['ansible_net_filesystems'])
    self.assertIn('GigabitEthernet0/0/0/0', ansible_facts['ansible_net_interfaces'].keys())
