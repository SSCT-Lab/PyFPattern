def main():
    spec = vmware_argument_spec()
    spec.update(dict(esxi_hostname=dict(required=True), vsan=dict(required=False, choices=['ensureObjectAccessibility', 'evacuateAllData', 'noAction']), evacuate=dict(required=False, type='bool', default=False), timeout=dict(required=False, default=0, type='int'), state=dict(required=False, default='present', choices=['present', 'absent'])))
    module = AnsibleModule(argument_spec=spec)
    if (not HAS_PYVMOMI):
        module.fail_json(msg='pyvmomi is required for this module')
    content = connect_to_api(module)
    host = find_hostsystem_by_name(content, module.params['esxi_hostname'])
    if (not host):
        module.fail_json(msg='Host not found in vCenter')
    if (module.params['state'] == 'present'):
        result = EnterMaintenanceMode(module, host)
    elif (module.params['state'] == 'absent'):
        result = ExitMaintenanceMode(module, host)
    module.exit_json(**result)