def main():
    module = AnsibleModule(argument_spec=dict(name=dict(required=True), port=dict(default=623, type='int'), user=dict(required=True, no_log=True), password=dict(required=True, no_log=True), state=dict(default='present', choices=['present', 'absent']), bootdev=dict(required=True, choices=['network', 'hd', 'safe', 'optical', 'setup', 'default']), persistent=dict(default=False, type='bool'), uefiboot=dict(default=False, type='bool')), supports_check_mode=True)
    if (command is None):
        module.fail_json(msg='the python pyghmi module is required')
    name = module.params['name']
    port = module.params['port']
    user = module.params['user']
    password = module.params['password']
    state = module.params['state']
    bootdev = module.params['bootdev']
    persistent = module.params['persistent']
    uefiboot = module.params['uefiboot']
    request = dict()
    if ((state == 'absent') and (bootdev == 'default')):
        module.fail_json(msg="The bootdev 'default' cannot be used with state 'absent'.")
    try:
        ipmi_cmd = command.Command(bmc=name, userid=user, password=password, port=port)
        module.debug(('ipmi instantiated - name: "%s"' % name))
        current = ipmi_cmd.get_bootdev()
        current.setdefault('uefimode', uefiboot)
        if ((state == 'present') and (current != dict(bootdev=bootdev, persistent=persistent, uefimode=uefiboot))):
            request = dict(bootdev=bootdev, uefiboot=uefiboot, persist=persistent)
        elif ((state == 'absent') and (current['bootdev'] == bootdev)):
            request = dict(bootdev='default')
        else:
            module.exit_json(changed=False, **current)
        if module.check_mode:
            response = dict(bootdev=request['bootdev'])
        else:
            response = ipmi_cmd.set_bootdev(**request)
        if ('error' in response):
            module.fail_json(msg=response['error'])
        if ('persist' in request):
            response['persistent'] = request['persist']
        if ('uefiboot' in request):
            response['uefimode'] = request['uefiboot']
        module.exit_json(changed=True, **response)
    except Exception as e:
        module.fail_json(msg=str(e))