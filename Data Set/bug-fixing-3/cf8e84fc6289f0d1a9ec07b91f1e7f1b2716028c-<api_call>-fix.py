def api_call(module, api_call_object):
    payload = get_payload_from_parameters(module.params)
    connection = Connection(module._socket_path)
    result = {
        'changed': False,
    }
    if module.check_mode:
        return result
    version = ((('v' + module.params['version']) + '/') if module.params.get('version') else '')
    payload_for_equals = {
        'type': api_call_object,
        'params': payload,
    }
    (equals_code, equals_response) = send_request(connection, version, 'equals', payload_for_equals)
    result['checkpoint_session_uid'] = connection.get_session_uid()
    if ((equals_code == 400) or (equals_code == 500)):
        module.fail_json(msg=equals_response)
    if ((equals_code == 404) and (equals_response['code'] == 'generic_err_command_not_found')):
        module.fail_json(msg='Relevant hotfix is not installed on Check Point server. See sk114661 on Check Point Support Center.')
    if (module.params['state'] == 'present'):
        if (equals_code == 200):
            if (not equals_response['equals']):
                (code, response) = send_request(connection, version, ('set-' + api_call_object), payload)
                if (code != 200):
                    module.fail_json(msg=response)
                handle_publish(module, connection, version)
                result['changed'] = True
                result[api_call_object] = response
            else:
                pass
        elif (equals_code == 404):
            (code, response) = send_request(connection, version, ('add-' + api_call_object), payload)
            if (code != 200):
                module.fail_json(msg=response)
            handle_publish(module, connection, version)
            result['changed'] = True
            result[api_call_object] = response
    elif (module.params['state'] == 'absent'):
        if (equals_code == 200):
            (code, response) = send_request(connection, version, ('delete-' + api_call_object), payload)
            if (code != 200):
                module.fail_json(msg=response)
            handle_publish(module, connection, version)
            result['changed'] = True
        elif (equals_code == 404):
            pass
    return result