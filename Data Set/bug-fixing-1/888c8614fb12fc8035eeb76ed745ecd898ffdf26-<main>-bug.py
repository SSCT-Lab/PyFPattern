

def main():
    module = AnsibleModule(argument_spec=dict(path=dict(required=True, aliases=['dest', 'destfile', 'name'], type='path'), regexp=dict(required=True), replace=dict(default='', type='str'), backup=dict(default=False, type='bool'), validate=dict(default=None, type='str')), add_file_common_args=True, supports_check_mode=True)
    params = module.params
    path = os.path.expanduser(params['path'])
    res_args = dict()
    if os.path.isdir(path):
        module.fail_json(rc=256, msg=('Path %s is a directory !' % path))
    if (not os.path.exists(path)):
        module.fail_json(rc=257, msg=('Path %s does not exist !' % path))
    else:
        f = open(path, 'rb')
        contents = to_text(f.read(), errors='surrogate_or_strict')
        f.close()
    mre = re.compile(params['regexp'], re.MULTILINE)
    result = re.subn(mre, params['replace'], contents, 0)
    if ((result[1] > 0) and (contents != result[0])):
        msg = ('%s replacements made' % result[1])
        changed = True
        if module._diff:
            res_args['diff'] = {
                'before_header': path,
                'before': contents,
                'after_header': path,
                'after': result[0],
            }
    else:
        msg = ''
        changed = False
    if (changed and (not module.check_mode)):
        if (params['backup'] and os.path.exists(path)):
            res_args['backup_file'] = module.backup_local(path)
        if (params['follow'] and os.path.islink(path)):
            path = os.path.realpath(path)
        write_changes(module, result[0], path)
    (res_args['msg'], res_args['changed']) = check_file_attrs(module, changed, msg)
    module.exit_json(**res_args)
