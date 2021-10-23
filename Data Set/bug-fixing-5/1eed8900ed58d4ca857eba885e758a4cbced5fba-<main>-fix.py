def main():
    argument_spec = influx.InfluxDb.influxdb_argument_spec()
    argument_spec.update(state=dict(default='present', type='str', choices=['present', 'absent']), user_name=dict(required=True, type='str'), user_password=dict(required=False, type='str', no_log=True), admin=dict(default='False', type='bool'))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    state = module.params['state']
    user_name = module.params['user_name']
    user_password = (module.params['user_password'] or '')
    admin = module.params['admin']
    influxdb = influx.InfluxDb(module)
    client = influxdb.connect_to_influxdb()
    user = find_user(module, client, user_name)
    if (state == 'present'):
        if user:
            changed = False
            if (not check_user_password(module, client, user_name, user_password)):
                set_user_password(module, client, user_name, user_password)
                changed = True
            try:
                if (admin and (not user['admin'])):
                    client.grant_admin_privileges(user_name)
                    changed = True
                elif ((not admin) and user['admin']):
                    client.revoke_admin_privileges(user_name)
                    changed = True
            except influx.exceptions.InfluxDBClientError as e:
                module.fail_json(msg=str(e))
            module.exit_json(changed=changed)
        else:
            create_user(module, client, user_name, user_password, admin)
    if (state == 'absent'):
        if user:
            drop_user(module, client, user_name)
        else:
            module.exit_json(changed=False)