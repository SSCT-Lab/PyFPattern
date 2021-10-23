def __init__(self, argument_spec):
    self.spec = argument_spec
    self.module = None
    self.init_module()
    self.local_file = self.module.params['local_file']
    self.remote_file = self.module.params['remote_file']
    self.file_system = self.module.params['file_system']
    self.host_is_ipv6 = validate_ip_v6_address(self.module.params['provider']['host'])
    self.transfer_result = None
    self.changed = False