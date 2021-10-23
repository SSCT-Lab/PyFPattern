def main():
    module = AnsibleModule(argument_spec=dict(_raw_params=dict(), _uses_shell=dict(type='bool', default=False), argv=dict(type='list'), chdir=dict(type='path'), executable=dict(), creates=dict(type='path'), removes=dict(type='path'), warn=dict(type='bool', default=True), stdin=dict(required=False)), supports_check_mode=True)
    shell = module.params['_uses_shell']
    chdir = module.params['chdir']
    executable = module.params['executable']
    args = module.params['_raw_params']
    argv = module.params['argv']
    creates = module.params['creates']
    removes = module.params['removes']
    warn = module.params['warn']
    stdin = module.params['stdin']
    if ((not shell) and executable):
        module.warn(("As of Ansible 2.4, the parameter 'executable' is no longer supported with the 'command' module. Not using '%s'." % executable))
        executable = None
    if (((not args) or (args.strip() == '')) and (not argv)):
        module.fail_json(rc=256, msg='no command given')
    if (args and argv):
        module.fail_json(rc=256, msg='only command or argv can be given, not both')
    if ((not shell) and args):
        args = shlex.split(args)
    args = (args or argv)
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
    startd = datetime.datetime.now()
    if (not module.check_mode):
        (rc, out, err) = module.run_command(args, executable=executable, use_unsafe_shell=shell, encoding=None, data=stdin)
    elif (creates or removes):
        rc = 0
        out = err = b'Command would have run if not in check mode'
    else:
        module.exit_json(msg='skipped, running in check mode', skipped=True)
    endd = datetime.datetime.now()
    delta = (endd - startd)
    result = dict(cmd=args, stdout=out.rstrip(b'\r\n'), stderr=err.rstrip(b'\r\n'), rc=rc, start=str(startd), end=str(endd), delta=str(delta), changed=True)
    if (rc != 0):
        module.fail_json(msg='non-zero return code', **result)
    module.exit_json(**result)