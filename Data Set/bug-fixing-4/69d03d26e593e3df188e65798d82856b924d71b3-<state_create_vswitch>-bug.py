def state_create_vswitch(self):
    vss_spec = vim.host.VirtualSwitch.Specification()
    vss_spec.numPorts = self.number_of_ports
    vss_spec.mtu = self.mtu
    if self.nic_name:
        if isinstance(self.nic_name, list):
            vss_spec.bridge = vim.host.VirtualSwitch.BondBridge(nicDevice=self.nic_name)
        else:
            vss_spec.bridge = vim.host.VirtualSwitch.BondBridge(nicDevice=[self.nic_name])
    self.host_system.configManager.networkSystem.AddVirtualSwitch(vswitchName=self.switch_name, spec=vss_spec)
    self.module.exit_json(changed=True)