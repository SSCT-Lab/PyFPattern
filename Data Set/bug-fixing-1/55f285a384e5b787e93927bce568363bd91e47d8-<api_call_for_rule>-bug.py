

def api_call_for_rule(module, api_call_object):
    is_access_rule = (True if ('access' in api_call_object) else False)
    payload = get_payload_from_parameters(module.params)
    connection = Connection(module._socket_path)
    result = {
        'changed': False,
    }
    if module.check_mode:
        return result
    version = ((('v' + module.params['version']) + '/') if module.params.get('version') else '')
    if is_access_rule:
        copy_payload_without_some_params = get_copy_payload_without_some_params(payload, ['action', 'position'])
    else:
        copy_payload_without_some_params = get_copy_payload_without_some_params(payload, ['position'])
    payload_for_equals = {
        'type': api_call_object,
        'params': copy_payload_without_some_params,
    }
    (equals_code, equals_response) = send_request(connection, version, 'equals', payload_for_equals)
    result['checkpoint_session_uid'] = connection.get_session_uid()
    if ((equals_code == 400) or (equals_code == 500)):
        module.fail_json(msg=equals_response)
    if (module.params['state'] == 'present'):
        if (equals_code == 200):
            if equals_response['equals']:
                if (not is_equals_with_all_params(payload, connection, version, api_call_object, is_access_rule)):
                    equals_response['equals'] = False
            if (not equals_response['equals']):
                if ('position' in payload):
                    payload['new-position'] = payload['position']
                    del payload['position']
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
            payload_for_delete = get_copy_payload_with_some_params(payload, delete_params)
            (code, response) = send_request(connection, version, ('delete-' + api_call_object), payload_for_delete)
            if (code != 200):
                module.fail_json(msg=response)
            handle_publish(module, connection, version)
            result['changed'] = True
        elif (equals_code == 404):
            pass
    return result
