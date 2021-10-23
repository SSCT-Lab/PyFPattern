

def __init__(self, module):
    super(PyVmomiHelper, self).__init__(module)
    self.port_group_name = self.params['portgroup_name']
    self.ip_address = self.params['network'].get('ip_address', None)
    self.subnet_mask = self.params['network'].get('subnet_mask', None)
    self.network_type = self.params['network']['type']
    self.mtu = self.params['mtu']
    self.enable_vsan = self.params['enable_vsan']
    self.enable_vmotion = self.params['enable_vmotion']
    self.enable_mgmt = self.params['enable_mgmt']
    self.enable_ft = self.params['enable_ft']
    self.vswitch_name = self.params['vswitch_name']
    self.vlan_id = self.params['vlan_id']
    self.esxi_host_name = self.params['esxi_hostname']
    self.esxi_host_obj = self.get_all_host_objs(esxi_host_name=self.esxi_host_name)[0]
    self.port_group_obj = self.get_port_group_by_name(host_system=self.esxi_host_obj, portgroup_name=self.port_group_name)
    if (not self.port_group_obj):
        module.fail_json(msg=('Portgroup name %s not found' % self.port_group_name))
    if (self.network_type == 'static'):
        if (not self.ip_address):
            module.fail_json(msg="network.ip_address is required parameter when network is set to 'static'.")
        if (not self.subnet_mask):
            module.fail_json(msg="network.subnet_mask is required parameter when network is set to 'static'.")
