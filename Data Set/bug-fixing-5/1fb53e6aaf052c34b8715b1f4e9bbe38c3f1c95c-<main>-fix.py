def main():
    module = AnsibleModule(argument_spec=dict(src=dict(required=True, type='path'), original_basename=dict(required=False, type='str'), dest=dict(required=True, type='path'), copy=dict(required=False, default=True, type='bool'), remote_src=dict(required=False, default=False, type='bool'), creates=dict(required=False, type='path'), list_files=dict(required=False, default=False, type='bool'), keep_newer=dict(required=False, default=False, type='bool'), exclude=dict(required=False, default=[], type='list'), extra_opts=dict(required=False, default=[], type='list'), validate_certs=dict(required=False, default=True, type='bool')), add_file_common_args=True, mutually_exclusive=[('copy', 'remote_src')], supports_check_mode=True)
    src = module.params['src']
    dest = module.params['dest']
    copy = module.params['copy']
    remote_src = module.params['remote_src']
    file_args = module.load_file_common_arguments(module.params)
    if (not os.path.exists(src)):
        if ((not remote_src) and copy):
            module.fail_json(msg=("Source '%s' failed to transfer" % src))
        elif ('://' in src):
            tempdir = os.path.dirname(os.path.realpath(__file__))
            package = os.path.join(tempdir, str(src.rsplit('/', 1)[1]))
            try:
                (rsp, info) = fetch_url(module, src)
                if (rsp is None):
                    raise Exception(info['msg'])
                f = open(package, 'w')
                while True:
                    data = rsp.read(BUFSIZE)
                    if (data == ''):
                        break
                    f.write(data)
                f.close()
                src = package
            except Exception:
                e = get_exception()
                module.fail_json(msg=('Failure downloading %s, %s' % (src, e)))
        else:
            module.fail_json(msg=("Source '%s' does not exist" % src))
    if (not os.access(src, os.R_OK)):
        module.fail_json(msg=("Source '%s' not readable" % src))
    try:
        if (os.path.getsize(src) == 0):
            module.fail_json(msg=("Invalid archive '%s', the file is 0 bytes" % src))
    except Exception:
        e = get_exception()
        module.fail_json(msg=("Source '%s' not readable" % src))
    if (not os.path.isdir(dest)):
        module.fail_json(msg=("Destination '%s' is not a directory" % dest))
    handler = pick_handler(src, dest, file_args, module)
    res_args = dict(handler=handler.__class__.__name__, dest=dest, src=src)
    check_results = handler.is_unarchived()
    if module.check_mode:
        res_args['changed'] = (not check_results['unarchived'])
    elif check_results['unarchived']:
        res_args['changed'] = False
    else:
        try:
            res_args['extract_results'] = handler.unarchive()
            if (res_args['extract_results']['rc'] != 0):
                module.fail_json(msg=('failed to unpack %s to %s' % (src, dest)), **res_args)
        except IOError:
            module.fail_json(msg=('failed to unpack %s to %s' % (src, dest)), **res_args)
        else:
            res_args['changed'] = True
    if check_results.get('diff', False):
        res_args['diff'] = {
            'prepared': check_results['diff'],
        }
    if (res_args.get('diff', True) and (not module.check_mode)):
        for filename in handler.files_in_archive:
            file_args['path'] = os.path.join(dest, filename)
            try:
                res_args['changed'] = module.set_fs_attributes_if_different(file_args, res_args['changed'])
            except (IOError, OSError):
                e = get_exception()
                module.fail_json(msg=('Unexpected error when accessing exploded file: %s' % str(e)), **res_args)
    if module.params['list_files']:
        res_args['files'] = handler.files_in_archive
    module.exit_json(**res_args)