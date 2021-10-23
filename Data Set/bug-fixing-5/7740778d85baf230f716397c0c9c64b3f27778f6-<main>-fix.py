def main():
    module = AnsibleModule(argument_spec=dict(name=dict(type='str', required=True), state=dict(type='str', default='present', choices=['absent', 'present'])), supports_check_mode=True)
    name = module.params['name']
    state = module.params['state']
    if (not os.path.exists('/etc/locale.gen')):
        if os.path.exists('/var/lib/locales/supported.d/'):
            ubuntuMode = True
        else:
            module.fail_json(msg='/etc/locale.gen and /var/lib/locales/supported.d/local are missing. Is the package "locales" installed?')
    else:
        ubuntuMode = False
    if (not is_available(name, ubuntuMode)):
        module.fail_json(msg="The locale you've entered is not available on your system.")
    if is_present(name):
        prev_state = 'present'
    else:
        prev_state = 'absent'
    changed = (prev_state != state)
    if module.check_mode:
        module.exit_json(changed=changed)
    else:
        if changed:
            try:
                if (ubuntuMode is False):
                    apply_change(state, name)
                else:
                    apply_change_ubuntu(state, name)
            except EnvironmentError as e:
                module.fail_json(msg=to_native(e), exitValue=e.errno)
        module.exit_json(name=name, changed=changed, msg='OK')