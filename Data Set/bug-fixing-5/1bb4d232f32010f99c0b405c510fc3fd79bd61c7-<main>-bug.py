def main():
    'entry point for module execution\n    '
    argument_spec = dict(command=dict(type='str', required=True), prompt=dict(type='list', required=False), answer=dict(type='str', required=False), sendonly=dict(type='bool', default=False, required=False))
    required_together = [['prompt', 'response']]
    module = AnsibleModule(argument_spec=argument_spec, required_together=required_together, supports_check_mode=True)
    if (module.check_mode and (not module.params['command'].startswith('show'))):
        module.fail_json(msg=('Only show commands are supported when using check_mode, not executing %s' % module.params['command']))
    warnings = list()
    result = {
        'changed': False,
        'warnings': warnings,
    }
    connection = Connection(module._socket_path)
    response = ''
    try:
        response = connection.get(**module.params)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc, errors='surrogate_then_replace'))
    if (not module.params['sendonly']):
        try:
            result['json'] = module.from_json(response)
        except ValueError:
            pass
        result.update({
            'stdout': response,
        })
    module.exit_json(**result)