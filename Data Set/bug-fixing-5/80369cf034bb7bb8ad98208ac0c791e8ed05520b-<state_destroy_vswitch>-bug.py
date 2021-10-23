def state_destroy_vswitch(self):
    '\n        Function to remove vSwitch from configuration\n\n        '
    results = dict(changed=False, result='')
    try:
        self.host_system.configManager.networkSystem.RemoveVirtualSwitch(self.vss.name)
        results['changed'] = True
        results['result'] = ("vSwitch '%s' removed successfully." % self.vss.name)
    except vim.fault.NotFound as vswitch_not_found:
        results['result'] = ("vSwitch '%s' not available. %s" % (self.switch, to_native(vswitch_not_found.msg)))
    except vim.fault.ResourceInUse as vswitch_in_use:
        self.module.fail_json(msg=("Failed to remove vSwitch '%s' as vSwitch is used by several virtual network adapters: %s" % (self.switch, to_native(vswitch_in_use.msg))))
    except vim.fault.HostConfigFault as host_config_fault:
        self.module.fail_json(msg=("Failed to remove vSwitch '%s' due to host configuration fault : %s" % (self.switch, to_native(host_config_fault.msg))))
    except Exception as generic_exc:
        self.module.fail_json(msg=("Failed to remove vSwitch '%s' due to generic exception : %s" % (self.switch, to_native(generic_exc))))
    self.module.exit_json(**results)