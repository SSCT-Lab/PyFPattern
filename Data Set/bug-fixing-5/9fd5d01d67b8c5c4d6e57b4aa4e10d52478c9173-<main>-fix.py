def main():
    module = AnsibleModule(supports_check_mode=True, argument_spec=dict(target=dict(required=False, default=None, type='str'), params=dict(required=False, default=None, type='dict'), chdir=dict(required=True, default=None, type='path'), file=dict(required=False, default=None, type='path')))
    make_path = module.get_bin_path('make', True)
    make_target = module.params['target']
    if (module.params['params'] is not None):
        make_parameters = [((k + '=') + str(v)) for (k, v) in iteritems(module.params['params'])]
    else:
        make_parameters = []
    if (module.params['file'] is not None):
        base_command = [make_path, '--file', module.params['file'], make_target]
    else:
        base_command = [make_path, make_target]
    base_command.extend(make_parameters)
    (rc, out, err) = run_command((base_command + ['--question']), module, check_rc=False)
    if module.check_mode:
        changed = (rc != 0)
    elif (rc == 0):
        changed = False
    else:
        (rc, out, err) = run_command(base_command, module, check_rc=True)
        changed = True
    module.exit_json(changed=changed, failed=False, stdout=out, stderr=err, target=module.params['target'], params=module.params['params'], chdir=module.params['chdir'], file=module.params['file'])