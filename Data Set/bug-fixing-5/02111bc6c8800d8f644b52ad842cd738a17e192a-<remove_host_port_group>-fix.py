def remove_host_port_group(self, host_system, portgroup_name, vswitch_name):
    '\n        Function to remove port group depending upon host system, port group name and vswitch name\n        Args:\n            host_system: Name of Host System\n            portgroup_name: Name of Portgroup\n            vswitch_name: Name of vSwitch\n\n        '
    changed = False
    desired_pgs = self.get_port_group_by_name(host_system=host_system, portgroup_name=portgroup_name, vswitch_name=vswitch_name)
    if desired_pgs:
        try:
            host_system.configManager.networkSystem.RemovePortGroup(pgName=self.portgroup_name)
            changed = True
        except vim.fault.NotFound as not_found:
            self.module.fail_json(msg=('Failed to remove Portgroup as it was not found: %s' % to_native(not_found.msg)))
        except vim.fault.ResourceInUse as resource_in_use:
            self.module.fail_json(msg=('Failed to remove Portgroup as it is in use: %s' % to_native(resource_in_use.msg)))
        except vim.fault.HostConfigFault as host_config_fault:
            self.module.fail_json(msg=('Failed to remove Portgroup due to configuration failures: %s' % to_native(host_config_fault.msg)))
        except Exception as generic_exception:
            self.module.fail_json(msg=('Failed to remove Portgroup due to generic exception : %s' % to_native(generic_exception)))
    return changed