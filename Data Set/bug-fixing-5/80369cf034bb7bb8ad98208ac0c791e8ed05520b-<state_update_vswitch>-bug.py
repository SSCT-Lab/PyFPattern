def state_update_vswitch(self):
    '\n        Function to update vSwitch\n\n        '
    results = dict(changed=False, result=("No change in vSwitch '%s'" % self.switch))
    vswitch_pnic_info = self.available_vswitches[self.switch]
    remain_pnic = []
    for desired_pnic in self.nics:
        if (desired_pnic not in vswitch_pnic_info['pnic']):
            remain_pnic.append(desired_pnic)
    diff = False
    all_nics = vswitch_pnic_info['pnic']
    if remain_pnic:
        all_nics += remain_pnic
        diff = True
    vss_spec = vim.host.VirtualSwitch.Specification()
    vss_spec.bridge = vim.host.VirtualSwitch.BondBridge(nicDevice=all_nics)
    vss_spec.numPorts = self.number_of_ports
    vss_spec.mtu = self.mtu
    if ((vswitch_pnic_info['mtu'] != self.mtu) or (vswitch_pnic_info['num_ports'] != self.number_of_ports)):
        diff = True
    try:
        if diff:
            network_mgr = self.host_system.configManager.networkSystem
            if network_mgr:
                network_mgr.UpdateVirtualSwitch(vswitchName=self.switch, spec=vss_spec)
                results['changed'] = True
                results['result'] = ("vSwitch '%s' is updated successfully" % self.switch)
            else:
                self.module.fail_json(msg='Failed to find network manager for ESXi system.')
    except vim.fault.ResourceInUse as resource_used:
        self.module.fail_json(msg=("Failed to update vSwitch '%s' as physical network adapter being bridged is already in use: %s" % (self.switch, to_native(resource_used.msg))))
    except vim.fault.NotFound as not_found:
        self.module.fail_json(msg=("Failed to update vSwitch with name '%s' as it does not exists: %s" % (self.switch, to_native(not_found.msg))))
    except vim.fault.HostConfigFault as host_config_fault:
        self.module.fail_json(msg=("Failed to update vSwitch '%s' due to host configuration fault : %s" % (self.switch, to_native(host_config_fault.msg))))
    except vmodl.fault.InvalidArgument as invalid_argument:
        self.module.fail_json(msg=("Failed to update vSwitch '%s', this can be due to either of following : 1. vSwitch Name exceeds the maximum allowed length, 2. Number of ports specified falls out of valid range, 3. Network policy is invalid, 4. Beacon configuration is invalid : %s" % (self.switch, to_native(invalid_argument.msg))))
    except vmodl.fault.SystemError as system_error:
        self.module.fail_json(msg=("Failed to update vSwitch '%s' due to : %s" % (self.switch, to_native(system_error.msg))))
    except vmodl.fault.NotSupported as not_supported:
        self.module.fail_json(msg=("Failed to update vSwitch '%s' as network adapter teaming policy is set but is not supported : %s" % (self.switch, to_native(not_supported.msg))))
    except Exception as generic_exc:
        self.module.fail_json(msg=("Failed to update vSwitch '%s' due to generic exception : %s" % (self.switch, to_native(generic_exc))))
    self.module.exit_json(**results)