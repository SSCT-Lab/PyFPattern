def create_host_port_group(self, host_system, portgroup_name, vlan_id, vswitch_name, network_policy):
    '\n        Function to create/update portgroup on given host using portgroup specifications\n        Args:\n            host_system: Name of Host System\n            portgroup_name: Name of Portgroup\n            vlan_id: The VLAN ID for ports using this port group.\n            vswitch_name: Name of vSwitch Name\n            network_policy: Network policy object\n        '
    desired_pgs = self.get_port_group_by_name(host_system=host_system, portgroup_name=portgroup_name, vswitch_name=vswitch_name)
    port_group = vim.host.PortGroup.Config()
    port_group.spec = vim.host.PortGroup.Specification()
    if (not desired_pgs):
        port_group.spec.name = portgroup_name
        port_group.spec.vlanId = vlan_id
        port_group.spec.vswitchName = vswitch_name
        port_group.spec.policy = network_policy
        try:
            host_system.configManager.networkSystem.AddPortGroup(portgrp=port_group.spec)
            self.changed = True
        except vim.fault.AlreadyExists as e:
            self.changed = False
        except vim.fault.NotFound as not_found:
            self.module.fail_json(msg=('Failed to add Portgroup as vSwitch was not found: %s' % to_native(not_found.msg)))
        except vim.fault.HostConfigFault as host_config_fault:
            self.module.fail_json(msg=('Failed to add Portgroup due to host system configuration failure : %s' % to_native(host_config_fault.msg)))
        except vmodl.fault.InvalidArgument as invalid_argument:
            self.module.fail_json(msg=('Failed to add Portgroup as VLAN id was not correct as per specifications: %s' % to_native(invalid_argument.msg)))
        except Exception as generic_exception:
            self.module.fail_json(msg=('Failed to add Portgroup due to generic exception : %s' % to_native(generic_exception)))
    else:
        self.changed = False
        if (desired_pgs[0].spec.vlanId != vlan_id):
            port_group.spec.vlanId = vlan_id
            self.changed = True
        if self.check_network_policy_diff(desired_pgs[0].spec.policy, network_policy):
            port_group.spec.policy = network_policy
            self.changed = True
        if self.changed:
            try:
                host_system.configManager.networkSystem.UpdatePortGroup(pgName=self.portgroup_name, portgrp=port_group.spec)
                self.changed = True
            except vim.fault.AlreadyExists as e:
                self.changed = False
            except vim.fault.NotFound as not_found:
                self.module.fail_json(msg=('Failed to update Portgroup as vSwitch was not found: %s' % to_native(not_found.msg)))
            except vim.fault.HostConfigFault as host_config_fault:
                self.module.fail_json(msg=('Failed to update Portgroup due to host system configuration failure : %s' % to_native(host_config_fault.msg)))
            except vmodl.fault.InvalidArgument as invalid_argument:
                self.module.fail_json(msg=('Failed to update Portgroup as VLAN id was not correct as per specifications: %s' % to_native(invalid_argument.msg)))
            except Exception as generic_exception:
                self.module.fail_json(msg=('Failed to update Portgroup due to generic exception : %s' % to_native(generic_exception)))
    return self.changed