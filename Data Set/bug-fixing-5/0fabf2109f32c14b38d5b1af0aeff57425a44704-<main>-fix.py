def main():
    module = AnsibleModule(argument_spec=dict(), supports_check_mode=True)
    module.run_command_environ_update = dict(LANG='C', LC_ALL='C')
    service_modules = (ServiceScanService, SystemctlScanService)
    all_services = {
        
    }
    incomplete_warning = False
    for svc_module in service_modules:
        svcmod = svc_module(module)
        svc = svcmod.gather_services()
        if (svc is not None):
            all_services.update(svc)
            if svcmod.incomplete_warning:
                incomplete_warning = True
    if (len(all_services) == 0):
        results = dict(skipped=True, msg='Failed to find any services. Sometimes this is due to insufficient privileges.')
    else:
        results = dict(ansible_facts=dict(services=all_services))
        if incomplete_warning:
            results['msg'] = 'WARNING: Could not find status for all services. Sometimes this is due to insufficient privileges.'
    module.exit_json(**results)