def state_create_vswitch(self):
    '\n        Create a virtual switch\n\n        Source from\n        https://github.com/rreubenur/pyvmomi-community-samples/blob/patch-1/samples/create_vswitch.py\n\n        '
    results = dict(changed=False, result='')
    vss_spec = vim.host.VirtualSwitch.Specification()
    vss_spec.numPorts = self.number_of_ports
    vss_spec.mtu = self.mtu
    if self.nics:
        vss_spec.bridge = vim.host.VirtualSwitch.BondBridge(nicDevice=self.nics)
    try:
        network_mgr = self.host_system.configManager.networkSystem
        if network_mgr:
            network_mgr.AddVirtualSwitch(vswitchName=self.switch, spec=vss_spec)
            results['changed'] = True
            results['result'] = ("vSwitch '%s' is created successfully" % self.switch)
        else:
            self.module.fail_json(msg='Failed to find network manager for ESXi system')
    except vim.fault.AlreadyExists as already_exists:
        results['result'] = ('vSwitch with name %s already exists: %s' % (self.switch, to_native(already_exists.msg)))
    except vim.fault.ResourceInUse as resource_used:
        self.module.fail_json(msg=("Failed to add vSwitch '%s' as physical network adapter being bridged is already in use: %s" % (self.switch, to_native(resource_used.msg))))
    except vim.fault.HostConfigFault as host_config_fault:
        self.module.fail_json(msg=("Failed to add vSwitch '%s' due to host configuration fault : %s" % (self.switch, to_native(host_config_fault.msg))))
    except vmodl.fault.InvalidArgument as invalid_argument:
        self.module.fail_json(msg=("Failed to add vSwitch '%s', this can be due to either of following : 1. vSwitch Name exceeds the maximum allowed length, 2. Number of ports specified falls out of valid range, 3. Network policy is invalid, 4. Beacon configuration is invalid : %s" % (self.switch, to_native(invalid_argument.msg))))
    except vmodl.fault.SystemError as system_error:
        self.module.fail_json(msg=("Failed to add vSwitch '%s' due to : %s" % (self.switch, to_native(system_error.msg))))
    except Exception as generic_exc:
        self.module.fail_json(msg=("Failed to add vSwitch '%s' due to generic exception : %s" % (self.switch, to_native(generic_exc))))
    self.module.exit_json(**results)