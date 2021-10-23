def __init__(self, module):
    super(PyVmomiHelper, self).__init__(module)
    if self.params['network']:
        self.network_type = self.params['network'].get('type')
        self.ip_address = self.params['network'].get('ip_address', None)
        self.subnet_mask = self.params['network'].get('subnet_mask', None)
        self.default_gateway = self.params['network'].get('default_gateway', None)
        self.tcpip_stack = self.params['network'].get('tcpip_stack')
    self.device = self.params['device']
    if ((self.network_type == 'dhcp') and (not self.device)):
        module.fail_json(msg="device is a required parameter when network type is set to 'dhcp'")
    self.mtu = self.params['mtu']
    self.enable_vsan = self.params['enable_vsan']
    self.enable_vmotion = self.params['enable_vmotion']
    self.enable_mgmt = self.params['enable_mgmt']
    self.enable_ft = self.params['enable_ft']
    self.enable_provisioning = self.params['enable_provisioning']
    self.enable_replication = self.params['enable_replication']
    self.enable_replication_nfc = self.params['enable_replication_nfc']
    self.vswitch_name = self.params['vswitch_name']
    self.vds_name = self.params['dvswitch_name']
    self.port_group_name = self.params['portgroup_name']
    self.esxi_host_name = self.params['esxi_hostname']
    hosts = self.get_all_host_objs(esxi_host_name=self.esxi_host_name)
    if hosts:
        self.esxi_host_obj = hosts[0]
    else:
        self.module.fail_json(msg='Failed to get details of ESXi server. Please specify esxi_hostname.')
    if (self.network_type == 'static'):
        if (self.module.params['state'] == 'absent'):
            pass
        elif (not self.ip_address):
            module.fail_json(msg="ip_address is a required parameter when network type is set to 'static'")
        elif (not self.subnet_mask):
            module.fail_json(msg="subnet_mask is a required parameter when network type is set to 'static'")
    if self.vswitch_name:
        self.port_group_obj = self.get_port_group_by_name(host_system=self.esxi_host_obj, portgroup_name=self.port_group_name, vswitch_name=self.vswitch_name)
        if (not self.port_group_obj):
            module.fail_json(msg=("Portgroup '%s' not found on vSS '%s'" % (self.port_group_name, self.vswitch_name)))
    elif self.vds_name:
        self.dv_switch_obj = find_dvs_by_name(self.content, self.vds_name)
        if (not self.dv_switch_obj):
            module.fail_json(msg=("vDS '%s' not found" % self.vds_name))
        self.port_group_obj = find_dvspg_by_name(self.dv_switch_obj, self.port_group_name)
        if (not self.port_group_obj):
            module.fail_json(msg=("Portgroup '%s' not found on vDS '%s'" % (self.port_group_name, self.vds_name)))
    if self.device:
        self.vnic = self.get_vmkernel_by_device(device_name=self.device)
    else:
        self.vnic = self.get_vmkernel_by_portgroup_new(port_group_name=self.port_group_name)
        if (not self.vnic):
            if (self.network_type == 'static'):
                self.vnic = self.get_vmkernel_by_ip(ip_address=self.ip_address)
            elif (self.network_type == 'dhcp'):
                self.vnic = self.get_vmkernel_by_device(device_name=self.device)