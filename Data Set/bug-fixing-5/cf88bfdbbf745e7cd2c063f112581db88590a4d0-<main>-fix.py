def main():
    spec = vmware_argument_spec()
    spec.update(dict(esxi_hostname=dict(type='str', required=True), vsan=dict(type='str', choices=['ensureObjectAccessibility', 'evacuateAllData', 'noAction']), evacuate=dict(type='bool', default=False), timeout=dict(default=0, type='int'), state=dict(required=False, default='present', choices=['present', 'absent'])))
    module = AnsibleModule(argument_spec=spec)
    host_maintenance_mgr = VmwareMaintenanceMgr(module=module)
    if (module.params['state'] == 'present'):
        host_maintenance_mgr.EnterMaintenanceMode()
    elif (module.params['state'] == 'absent'):
        host_maintenance_mgr.ExitMaintenanceMode()