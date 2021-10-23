def main():
    argument_spec = purefa_argument_spec()
    argument_spec.update(dict(name=dict(required=True, type='str'), role=dict(type='str', choices=['readonly', 'storage_admin', 'array_admin']), state=dict(type='str', default='present', choices=['absent', 'present']), password=dict(type='str', no_log=True), old_password=dict(type='str', no_log=True), api=dict(type='bool', default=False)))
    module = AnsibleModule(argument_spec, supports_check_mode=False)
    state = module.params['state']
    array = get_system(module)
    if (state == 'absent'):
        delete_user(module, array)
    elif (state == 'present'):
        create_user(module, array)
    else:
        module.exit_json(changed=False)