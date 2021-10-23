def main():
    module = AnsibleModule(argument_spec=dict(name=dict(required=True), force=dict(required=False, type='bool', default=False), state=dict(default='present', choices=['absent', 'present'])), supports_check_mode=True)
    name = module.params['name']
    if ((name == 'cgi') and _run_threaded(module)):
        module.fail_json(msg=('Your MPM seems to be threaded. No automatic actions on module %s possible.' % name))
    if (module.params['state'] in ['present', 'absent']):
        _set_state(module, module.params['state'])