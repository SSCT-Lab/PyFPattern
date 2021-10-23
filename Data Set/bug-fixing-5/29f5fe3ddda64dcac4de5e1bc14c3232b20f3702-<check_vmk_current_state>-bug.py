def check_vmk_current_state(self):
    self.host_system = find_hostsystem_by_name(self.content, self.esxi_hostname)
    for vnic in self.host_system.configManager.networkSystem.networkInfo.vnic:
        if (vnic.device == self.device):
            if (vnic.spec.distributedVirtualPort is None):
                if (vnic.portgroup == self.current_portgroup_name):
                    return 'migrate_vss_vds'
            else:
                dvs = find_dvs_by_name(self.content, self.current_switch_name)
                if (dvs is None):
                    return 'migrated'
                if (vnic.spec.distributedVirtualPort.switchUuid == dvs.uuid):
                    return 'migrate_vds_vss'