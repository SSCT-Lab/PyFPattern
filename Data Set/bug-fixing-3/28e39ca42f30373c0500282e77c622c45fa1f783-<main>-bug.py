def main():
    module = AnsibleModule(argument_spec=dict(command=dict(required=True), chdir=dict(), creates=dict(), removes=dict(), responses=dict(type='dict', required=True), timeout=dict(type='int', default=30), echo=dict(type='bool', default=False)))
    if (not HAS_PEXPECT):
        module.fail_json(msg='The pexpect python module is required')
    chdir = module.params['chdir']
    args = module.params['command']
    creates = module.params['creates']
    removes = module.params['removes']
    responses = module.params['responses']
    timeout = module.params['timeout']
    echo = module.params['echo']
    events = dict()
    for (key, value) in responses.items():
        if isinstance(value, list):
            response = response_closure(module, key, value)
        else:
            response = ('%s\n' % value.rstrip('\n').decode())
        events[key.decode()] = response
    if (args.strip() == ''):
        module.fail_json(rc=256, msg='no command given')
    if chdir:
        chdir = os.path.abspath(os.path.expanduser(chdir))
        os.chdir(chdir)
    if creates:
        v = os.path.expanduser(creates)
        if os.path.exists(v):
            module.exit_json(cmd=args, stdout=('skipped, since %s exists' % v), changed=False, rc=0)
    if removes:
        v = os.path.expanduser(removes)
        if (not os.path.exists(v)):
            module.exit_json(cmd=args, stdout=('skipped, since %s does not exist' % v), changed=False, rc=0)
    startd = datetime.datetime.now()
    try:
        try:
            (out, rc) = pexpect.run(args, timeout=timeout, withexitstatus=True, events=events, cwd=chdir, echo=echo, encoding='utf-8')
        except TypeError:
            (out, rc) = pexpect.runu(args, timeout=timeout, withexitstatus=True, events=events, cwd=chdir, echo=echo)
    except (TypeError, AttributeError):
        e = get_exception()
        module.fail_json(msg=('Insufficient version of pexpect installed (%s), this module requires pexpect>=3.3. Error was %s' % (pexpect.__version__, e)))
    except pexpect.ExceptionPexpect:
        e = get_exception()
        module.fail_json(msg=('%s' % e))
    endd = datetime.datetime.now()
    delta = (endd - startd)
    if (out is None):
        out = ''
    ret = dict(cmd=args, stdout=out.rstrip('\r\n'), rc=rc, start=str(startd), end=str(endd), delta=str(delta), changed=True)
    if (rc is not None):
        module.exit_json(**ret)
    else:
        ret['msg'] = 'command exceeded timeout'
        module.fail_json(**ret)