

def ensure(self):
    'Manage IPv6 for an ESXi host system'
    results = dict(changed=False, result=dict())
    desired_state = self.module.params['state']
    host_change_list = []
    for host in self.hosts:
        changed = False
        results['result'][host.name] = dict(msg='')
        host_network_system = host.configManager.networkSystem
        host_network_info = host_network_system.networkInfo
        if (desired_state == 'enabled'):
            if host_network_info.atBootIpV6Enabled:
                if host_network_info.ipV6Enabled:
                    results['result'][host.name]['msg'] = ("IPv6 is already enabled and active for host '%s'" % host.name)
                if (not host_network_info.ipV6Enabled):
                    results['result'][host.name]['msg'] = ("IPv6 is already enabled for host '%s', but a reboot is required!" % host.name)
            elif (not self.module.check_mode):
                try:
                    config = vim.host.NetworkConfig()
                    config.ipV6Enabled = True
                    host_network_system.UpdateNetworkConfig(config, 'modify')
                    changed = True
                    results['result'][host.name]['changed'] = True
                    results['result'][host.name]['msg'] = ("IPv6 enabled for host '%s'" % host.name)
                except (vim.fault.AlreadyExists, vim.fault.NotFound):
                    self.module.fail_json(msg=("Network entity specified in the configuration for host '%s' already exists" % host.name))
                except vmodl.fault.InvalidArgument as invalid_argument:
                    self.module.fail_json(msg=("Invalid parameter specified for host '%s' : %s" % (host.name, to_native(invalid_argument.msg))))
                except vim.fault.HostConfigFault as config_fault:
                    self.module.fail_json(msg=("Failed to enable IPv6 for host '%s' due to : %s" % (host.name, to_native(config_fault.msg))))
                except vmodl.fault.NotSupported as not_supported:
                    self.module.fail_json(msg=("Failed to enable IPv6 for host '%s' due to : %s" % (host.name, to_native(not_supported.msg))))
                except (vmodl.RuntimeFault, vmodl.MethodFault) as runtime_fault:
                    self.module.fail_json(msg=("Failed to enable IPv6 for host '%s' due to : %s" % (host.name, to_native(runtime_fault.msg))))
            else:
                changed = True
                results['result'][host.name]['changed'] = True
                results['result'][host.name]['msg'] = ("IPv6 will be enabled for host '%s'" % host.name)
        elif (desired_state == 'disabled'):
            if (not host_network_info.atBootIpV6Enabled):
                if (not host_network_info.ipV6Enabled):
                    results['result'][host.name]['msg'] = ("IPv6 is already disabled for host '%s'" % host.name)
                if host_network_info.ipV6Enabled:
                    changed = True
                    results['result'][host.name]['msg'] = ("IPv6 is already disabled for host '%s', but a reboot is required!" % host.name)
            elif (not self.module.check_mode):
                try:
                    config = vim.host.NetworkConfig()
                    config.ipV6Enabled = False
                    host_network_system.UpdateNetworkConfig(config, 'modify')
                    changed = True
                    results['result'][host.name]['changed'] = True
                    results['result'][host.name]['msg'] = ("IPv6 disabled for host '%s'" % host.name)
                except (vim.fault.AlreadyExists, vim.fault.NotFound):
                    self.module.fail_json(msg=("Network entity specified in the configuration for host '%s' already exists" % host.name))
                except vmodl.fault.InvalidArgument as invalid_argument:
                    self.module.fail_json(msg=("Invalid parameter specified for host '%s' : %s" % (host.name, to_native(invalid_argument.msg))))
                except vim.fault.HostConfigFault as config_fault:
                    self.module.fail_json(msg=("Failed to disable IPv6 for host '%s' due to : %s" % (host.name, to_native(config_fault.msg))))
                except vmodl.fault.NotSupported as not_supported:
                    self.module.fail_json(msg=("Failed to disable IPv6 for host '%s' due to : %s" % (host.name, to_native(not_supported.msg))))
                except (vmodl.RuntimeFault, vmodl.MethodFault) as runtime_fault:
                    self.module.fail_json(msg=("Failed to disable IPv6 for host '%s' due to : %s" % (host.name, to_native(runtime_fault.msg))))
            else:
                changed = True
                results['result'][host.name]['changed'] = True
                results['result'][host.name]['msg'] = ("IPv6 will be disabled for host '%s'" % host.name)
        host_change_list.append(changed)
    if any(host_change_list):
        results['changed'] = True
    self.module.exit_json(**results)
