def main():
    module = AnsibleModule(argument_spec=dict(_raw_params=dict(), _uses_shell=dict(type='bool', default=False), chdir=dict(type='path'), executable=dict(), creates=dict(type='path'), removes=dict(type='path'), warn=dict(type='bool', default=True)))
    shell = module.params['_uses_shell']
    chdir = module.params['chdir']
    executable = module.params['executable']
    args = module.params['_raw_params']
    creates = module.params['creates']
    removes = module.params['removes']
    warn = module.params['warn']
    if ((not shell) and executable):
        module.warn(("As of Ansible 2.4, the parameter 'executable' is no longer supported with the 'command' module. Not using '%s'." % executable))
        executable = None
    if (args.strip() == ''):
        module.fail_json(rc=256, msg='no command given')
    if chdir:
        chdir = os.path.abspath(chdir)
        os.chdir(chdir)
    if creates:
        if glob.glob(creates):
            module.exit_json(cmd=args, stdout=('skipped, since %s exists' % creates), changed=False, rc=0)
    if removes:
        if (not glob.glob(removes)):
            module.exit_json(cmd=args, stdout=('skipped, since %s does not exist' % removes), changed=False, rc=0)
    if warn:
        check_command(module, args)
    if (not shell):
        args = shlex.split(args)
    startd = datetime.datetime.now()
    (rc, out, err) = module.run_command(args, executable=executable, use_unsafe_shell=shell, encoding=None)
    endd = datetime.datetime.now()
    delta = (endd - startd)
    if (out is None):
        out = b('')
    if (err is None):
        err = b('')
    result = dict(cmd=args, stdout=out.rstrip(b('\r\n')), stderr=err.rstrip(b('\r\n')), rc=rc, start=str(startd), end=str(endd), delta=str(delta), changed=True)
    if (rc != 0):
        module.fail_json(msg='non-zero return code', **result)
    module.exit_json(**result)