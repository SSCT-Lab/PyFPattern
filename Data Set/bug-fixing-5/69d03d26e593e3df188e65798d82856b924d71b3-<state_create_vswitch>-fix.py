def state_create_vswitch(self):
    vss_spec = vim.host.VirtualSwitch.Specification()
    vss_spec.numPorts = self.number_of_ports
    vss_spec.mtu = self.mtu
    if self.nics:
        vss_spec.bridge = vim.host.VirtualSwitch.BondBridge(nicDevice=self.nics)
    self.host_system.configManager.networkSystem.AddVirtualSwitch(vswitchName=self.switch, spec=vss_spec)
    self.module.exit_json(changed=True)