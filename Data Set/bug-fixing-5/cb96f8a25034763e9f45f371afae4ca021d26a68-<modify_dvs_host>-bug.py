def modify_dvs_host(self, operation):
    spec = vim.DistributedVirtualSwitch.ConfigSpec()
    spec.configVersion = self.dv_switch.config.configVersion
    spec.host = [vim.dvs.HostMember.ConfigSpec()]
    spec.host[0].operation = operation
    spec.host[0].host = self.host
    if (operation in ('edit', 'add')):
        spec.host[0].backing = vim.dvs.HostMember.PnicBacking()
        count = 0
        for nic in self.vmnics:
            spec.host[0].backing.pnicSpec.append(vim.dvs.HostMember.PnicSpec())
            spec.host[0].backing.pnicSpec[count].pnicDevice = nic
            spec.host[0].backing.pnicSpec[count].uplinkPortgroupKey = self.uplink_portgroup.key
            count += 1
    task = self.dv_switch.ReconfigureDvs_Task(spec)
    (changed, result) = wait_for_task(task)
    return (changed, result)