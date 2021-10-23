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
            self.module.fail_json(msg=('Failed to add Portgroup as it already exists: %s' % e.msg))
        except vim.fault.NotFound as e:
            self.module.fail_json(msg=('Failed to add Portgroup as vSwitch was not found: %s' % e.msg))
        except vim.fault.HostConfigFault as e:
            self.module.fail_json(msg=('Failed to add Portgroup due to host system configuration failure : %s' % e.msg))
        except vmodl.fault.InvalidArgument as e:
            self.module.fail_json(msg=('Failed to add Portgroup as VLAN id was not correct as per specifications: %s' % e.msg))
    else:
        if (desired_pgs[0].spec.vlanId != vlan_id):
            port_group.spec.vlanId = vlan_id
            self.changed = True
        if self.check_network_policy_diff(desired_pgs[0].spec.policy, network_policy):
            port_group.spec.policy = network_policy
            self.changed = True
        if self.changed:
            try:
                host_system.configManager.networkSystem.UpdatePortGroup(pgName=self.portgroup_name, portgrp=port_group.spec)
            except vim.fault.AlreadyExists as e:
                self.module.fail_json(msg=('Failed to update Portgroup as it conflicts with already existing Portgroup: %s' % e.msg))
            except vim.fault.NotFound as e:
                self.module.fail_json(msg=('Failed to update Portgroup as vSwitch was not found: %s' % e.msg))
            except vim.fault.HostConfigFault as e:
                self.module.fail_json(msg=('Failed to update Portgroup due to host system configuration failure : %s' % e.msg))
            except vmodl.fault.InvalidArgument as e:
                self.module.fail_json(msg=('Failed to update Portgroup as VLAN id was not correct as per specifications: %s' % e.msg))
        self.changed = False