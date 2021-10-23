def state_migrate_vss_vds(self):
    host_network_system = self.host_system.configManager.networkSystem
    dv_switch = find_dvs_by_name(self.content, self.migrate_switch_name)
    pg = find_dvspg_by_name(dv_switch, self.migrate_portgroup_name)
    config = vim.host.NetworkConfig()
    config.portgroup = [self.create_port_group_config()]
    config.vnic = [self.create_host_vnic_config(dv_switch.uuid, pg.key)]
    host_network_system.UpdateNetworkConfig(config, 'modify')
    self.module.exit_json(changed=True)