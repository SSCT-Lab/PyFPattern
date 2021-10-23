def main():
    module = AnsibleModule(argument_spec=dict(name=dict(required=True), state=dict(required=True, choices=['present', 'absent', 'opts_present', 'opts_absent']), backing_device=dict(default=None), password=dict(default=None, type='path'), opts=dict(default=None), path=dict(default='/etc/crypttab', type='path')), supports_check_mode=True)
    backing_device = module.params['backing_device']
    password = module.params['password']
    opts = module.params['opts']
    state = module.params['state']
    path = module.params['path']
    name = module.params['name']
    if name.startswith('/dev/mapper/'):
        name = name[len('/dev/mapper/'):]
    if ((state != 'absent') and (backing_device is None) and (password is None) and (opts is None)):
        module.fail_json(msg="expected one or more of 'backing_device', 'password' or 'opts'", **module.params)
    if (('opts' in state) and ((backing_device is not None) or (password is not None))):
        module.fail_json(msg=("cannot update 'backing_device' or 'password' when state=%s" % state), **module.params)
    for (arg_name, arg) in (('name', name), ('backing_device', backing_device), ('password', password), ('opts', opts)):
        if ((arg is not None) and ((' ' in arg) or ('\t' in arg) or (arg == ''))):
            module.fail_json(msg=("invalid '%s': contains white space or is empty" % arg_name), **module.params)
    try:
        crypttab = Crypttab(path)
        existing_line = crypttab.match(name)
    except Exception as e:
        module.fail_json(msg=('failed to open and parse crypttab file: %s' % to_native(e)), exception=traceback.format_exc(), **module.params)
    if (('present' in state) and (existing_line is None) and (backing_device is None)):
        module.fail_json(msg="'backing_device' required to add a new entry", **module.params)
    (changed, reason) = (False, '?')
    if (state == 'absent'):
        if (existing_line is not None):
            (changed, reason) = existing_line.remove()
    elif (state == 'present'):
        if (existing_line is not None):
            (changed, reason) = existing_line.set(backing_device, password, opts)
        else:
            (changed, reason) = crypttab.add(Line(None, name, backing_device, password, opts))
    elif (state == 'opts_present'):
        if (existing_line is not None):
            (changed, reason) = existing_line.opts.add(opts)
        else:
            (changed, reason) = crypttab.add(Line(None, name, backing_device, password, opts))
    elif (state == 'opts_absent'):
        if (existing_line is not None):
            (changed, reason) = existing_line.opts.remove(opts)
    if (changed and (not module.check_mode)):
        try:
            f = open(path, 'wb')
            f.write(to_bytes(crypttab, errors='surrogate_or_strict'))
        finally:
            f.close()
    module.exit_json(changed=changed, msg=reason, **module.params)