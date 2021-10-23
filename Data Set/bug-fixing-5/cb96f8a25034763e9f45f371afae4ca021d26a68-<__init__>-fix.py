def __init__(self, module):
    super(VMwareDvsHost, self).__init__(module)
    self.dv_switch = None
    self.uplink_portgroup = None
    self.host = None
    self.dv_switch = None
    self.nic = None
    self.state = self.module.params['state']
    self.switch_name = self.module.params['switch_name']
    self.esxi_hostname = self.module.params['esxi_hostname']
    self.vmnics = self.module.params['vmnics']