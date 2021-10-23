def main():
    'entry point for module execution\n    '
    argument_spec = dict(path=dict(required=True), content=dict(), method=dict(choices=['post', 'put', 'patch', 'delete'], default='post'), format=dict(choices=['json', 'xml'], default='json'))
    required_if = [['method', 'post', ['content']], ['method', 'put', ['content']], ['method', 'patch', ['content']]]
    module = AnsibleModule(argument_spec=argument_spec, required_if=required_if, supports_check_mode=True)
    path = module.params['path']
    candidate = module.params['content']
    method = module.params['method']
    format = module.params['format']
    if isinstance(candidate, string_types):
        candidate = json.loads(candidate)
    warnings = list()
    result = {
        'changed': False,
        'warnings': warnings,
    }
    running = None
    response = None
    commit = (not module.check_mode)
    try:
        running = restconf.get(module, path, output=format)
    except ConnectionError as exc:
        if (exc.code == 404):
            running = None
        else:
            module.fail_json(msg=to_text(exc), code=exc.code)
    try:
        if (method == 'delete'):
            if running:
                if commit:
                    response = restconf.edit_config(module, path=path, method='DELETE')
                result['changed'] = True
            else:
                warnings.append(("delete not executed as resource '%s' does not exist" % path))
        else:
            if running:
                if (method == 'post'):
                    module.fail_json(msg=("resource '%s' already exist" % path), code=409)
                diff = dict_diff(running, candidate)
                result['candidate'] = candidate
                result['running'] = running
            else:
                method = 'POST'
                diff = candidate
            if diff:
                if module._diff:
                    result['diff'] = {
                        'prepared': diff,
                        'before': candidate,
                        'after': running,
                    }
                if commit:
                    response = restconf.edit_config(module, path=path, content=diff, method=method.upper(), format=format)
                result['changed'] = True
    except ConnectionError as exc:
        module.fail_json(msg=str(exc), code=exc.code)
    module.exit_json(**result)