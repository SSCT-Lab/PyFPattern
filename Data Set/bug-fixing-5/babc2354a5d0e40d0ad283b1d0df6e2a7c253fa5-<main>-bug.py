def main():
    module = AnsibleModule(argument_spec=dict(path=dict(required=True, aliases=['dest', 'destfile', 'name'], type='path'), state=dict(default='present', choices=['absent', 'present']), regexp=dict(default=None), line=dict(aliases=['value']), insertafter=dict(default=None), insertbefore=dict(default=None), backrefs=dict(default=False, type='bool'), create=dict(default=False, type='bool'), backup=dict(default=False, type='bool'), validate=dict(default=None, type='str')), mutually_exclusive=[['insertbefore', 'insertafter']], add_file_common_args=True, supports_check_mode=True)
    params = module.params
    create = params['create']
    backup = params['backup']
    backrefs = params['backrefs']
    path = params['path']
    b_path = to_bytes(path, errors='surrogate_or_strict')
    if os.path.isdir(b_path):
        module.fail_json(rc=256, msg=('Path %s is a directory !' % path))
    if (params['state'] == 'present'):
        if (backrefs and (params['regexp'] is None)):
            module.fail_json(msg='regexp= is required with backrefs=true')
        if (params.get('line', None) is None):
            module.fail_json(msg='line= is required with state=present')
        (ins_bef, ins_aft) = (params['insertbefore'], params['insertafter'])
        if ((ins_bef is None) and (ins_aft is None)):
            ins_aft = 'EOF'
        line = params['line']
        present(module, path, params['regexp'], line, ins_aft, ins_bef, create, backup, backrefs)
    else:
        if ((params['regexp'] is None) and (params.get('line', None) is None)):
            module.fail_json(msg='one of line= or regexp= is required with state=absent')
        absent(module, path, params['regexp'], params.get('line', None), backup)