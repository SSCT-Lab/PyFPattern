def main():
    module = AnsibleModule(argument_spec=dict(name=dict(required=True), state=dict(choices=['running', 'started', 'stopped', 'restarted', 'reloaded']), sleep=dict(required=False, type='int', default=None), pattern=dict(required=False, default=None), enabled=dict(type='bool'), runlevel=dict(required=False, default='default'), arguments=dict(aliases=['args'], default='')), supports_check_mode=True, required_one_of=[['state', 'enabled']])
    service = Service(module)
    module.debug(('Service instantiated - platform %s' % service.platform))
    if service.distribution:
        module.debug(('Service instantiated - distribution %s' % service.distribution))
    rc = 0
    out = ''
    err = ''
    result = {
        
    }
    result['name'] = service.name
    service.get_service_tools()
    if (service.module.params['enabled'] is not None):
        service.service_enable()
        result['enabled'] = service.enable
    if (module.params['state'] is None):
        result['changed'] = service.changed
        module.exit_json(**result)
    result['state'] = service.state
    if service.pattern:
        service.check_ps()
    else:
        service.get_service_status()
    service.check_service_changed()
    (rc, out, err) = service.modify_service_state()
    if (rc != 0):
        if (err and ('Job is already running' in err)):
            pass
        elif err:
            module.fail_json(msg=err)
        else:
            module.fail_json(msg=out)
    result['changed'] = (service.changed | service.svc_change)
    if (service.module.params['enabled'] is not None):
        result['enabled'] = service.module.params['enabled']
    if (not service.module.params['state']):
        status = service.get_service_status()
        if (status is None):
            result['state'] = 'absent'
        elif (status is False):
            result['state'] = 'started'
        else:
            result['state'] = 'stopped'
    elif (service.module.params['state'] in ['started', 'restarted', 'running', 'reloaded']):
        result['state'] = 'started'
    else:
        result['state'] = 'stopped'
    module.exit_json(**result)