def __init__(self, module):
    self.host_system = None
    self.content = None
    self.vss = None
    self.module = module
    self.switch_name = module.params['switch_name']
    self.number_of_ports = module.params['number_of_ports']
    self.nic_name = module.params['nic_name']
    self.mtu = module.params['mtu']
    self.state = module.params['state']
    self.content = connect_to_api(self.module)