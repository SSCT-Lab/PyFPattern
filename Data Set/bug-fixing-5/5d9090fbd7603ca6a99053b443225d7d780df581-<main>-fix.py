def main():
    module = AnsibleModule(argument_spec=dict(name=dict(required=True), state=dict(required=False, choices=['present', 'absent'], default='present'), type=dict(required=True), autostart=dict(required=False, type='bool', default=False), extra_info=dict(required=False, default=''), port_open=dict(required=False, type='bool', default=False), login_name=dict(required=True), login_password=dict(required=True, no_log=True), machine=dict(required=False, default=None)), supports_check_mode=True)
    app_name = module.params['name']
    app_type = module.params['type']
    app_state = module.params['state']
    if module.params['machine']:
        (session_id, account) = webfaction.login(module.params['login_name'], module.params['login_password'], module.params['machine'])
    else:
        (session_id, account) = webfaction.login(module.params['login_name'], module.params['login_password'])
    app_list = webfaction.list_apps(session_id)
    app_map = dict([(i['name'], i) for i in app_list])
    existing_app = app_map.get(app_name)
    result = {
        
    }
    if (app_state == 'present'):
        if existing_app:
            if (existing_app['type'] != app_type):
                module.fail_json(msg='App already exists with different type. Please fix by hand.')
            module.exit_json(changed=False, result=existing_app)
        if (not module.check_mode):
            result.update(webfaction.create_app(session_id, app_name, app_type, module.boolean(module.params['autostart']), module.params['extra_info'], module.boolean(module.params['port_open'])))
    elif (app_state == 'absent'):
        if (not existing_app):
            module.exit_json(changed=False)
        if (not module.check_mode):
            result.update(webfaction.delete_app(session_id, app_name))
    else:
        module.fail_json(msg='Unknown state specified: {}'.format(app_state))
    module.exit_json(changed=True, result=result)