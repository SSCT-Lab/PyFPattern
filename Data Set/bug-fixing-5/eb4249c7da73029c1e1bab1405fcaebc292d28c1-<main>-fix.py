def main():
    module = AnsibleModule(argument_spec=dict(name=dict(type='str', required=True), state=dict(type='str', default='present', choices=['absent', 'present']), params=dict(type='str', default='')), supports_check_mode=True)
    name = module.params['name']
    params = module.params['params']
    state = module.params['state']
    result = dict(changed=False, name=name, params=params, state=state)
    try:
        present = False
        with open('/proc/modules') as modules:
            module_name = (name.replace('-', '_') + ' ')
            for line in modules:
                if line.startswith(module_name):
                    present = True
                    break
        if (not present):
            command = [module.get_bin_path('uname', True), '-r']
            (rc, uname_kernel_release, err) = module.run_command(command)
            module_file = (('/' + name) + '.ko')
            builtin_path = os.path.join('/lib/modules/', uname_kernel_release.strip(), 'modules.builtin')
            with open(builtin_path) as builtins:
                for line in builtins:
                    if line.endswith(module_file):
                        present = True
                        break
    except IOError as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc(), **result)
    if (state == 'present'):
        if (not present):
            if (not module.check_mode):
                command = [module.get_bin_path('modprobe', True), name]
                command.extend(shlex.split(params))
                (rc, out, err) = module.run_command(command)
                if (rc != 0):
                    module.fail_json(msg=err, rc=rc, stdout=out, stderr=err, **result)
            result['changed'] = True
    elif (state == 'absent'):
        if present:
            if (not module.check_mode):
                (rc, out, err) = module.run_command([module.get_bin_path('modprobe', True), '-r', name])
                if (rc != 0):
                    module.fail_json(msg=err, rc=rc, stdout=out, stderr=err, **result)
            result['changed'] = True
    module.exit_json(**result)