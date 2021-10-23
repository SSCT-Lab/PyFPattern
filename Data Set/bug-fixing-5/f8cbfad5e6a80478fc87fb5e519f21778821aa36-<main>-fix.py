def main():
    module = AnsibleModule(argument_spec=dict(path=dict(required=True, aliases=['dest'], type='path'), section=dict(required=True), option=dict(required=False), value=dict(required=False), backup=dict(default='no', type='bool'), state=dict(default='present', choices=['present', 'absent']), no_extra_spaces=dict(required=False, default=False, type='bool'), create=dict(default=True, type='bool')), add_file_common_args=True, supports_check_mode=True)
    path = module.params['path']
    section = module.params['section']
    option = module.params['option']
    value = module.params['value']
    state = module.params['state']
    backup = module.params['backup']
    no_extra_spaces = module.params['no_extra_spaces']
    create = module.params['create']
    (changed, backup_file, diff, msg) = do_ini(module, path, section, option, value, state, backup, no_extra_spaces, create)
    if ((not module.check_mode) and os.path.exists(path)):
        file_args = module.load_file_common_arguments(module.params)
        changed = module.set_fs_attributes_if_different(file_args, changed)
    results = {
        'changed': changed,
        'msg': msg,
        'path': path,
        'diff': diff,
    }
    if (backup_file is not None):
        results['backup_file'] = backup_file
    module.exit_json(**results)