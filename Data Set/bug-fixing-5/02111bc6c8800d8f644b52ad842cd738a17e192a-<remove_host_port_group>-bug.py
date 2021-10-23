def remove_host_port_group(self, host_system, portgroup_name, vswitch_name):
    '\n        Function to remove port group depending upon host system, port group name and vswitch name\n        Args:\n            host_system: Name of Host System\n            portgroup_name: Name of Portgroup\n            vswitch_name: Name of vSwitch\n\n        '
    desired_pgs = self.get_port_group_by_name(host_system=host_system, portgroup_name=portgroup_name, vswitch_name=vswitch_name)
    if desired_pgs:
        try:
            host_system.configManager.networkSystem.RemovePortGroup(pgName=self.portgroup_name)
            self.changed = True
        except vim.fault.NotFound as e:
            self.module.fail_json(msg=('Failed to remove Portgroup as it was not found: %s' % e.msg))
        except vim.fault.ResourceInUse as e:
            self.module.fail_json(msg=('Failed to remove Portgroup as it is in use: %s' % e.msg))
        except vim.fault.HostConfigFault as e:
            self.module.fail_json(msg=('Failed to remove Portgroup due to configuration failures: %s' % e.msg))
    else:
        self.changed = False