

def axapi_authenticate_v3(module, base_url, username, password):
    url = base_url
    auth_payload = {
        'credentials': {
            'username': username,
            'password': password,
        },
    }
    result = axapi_call_v3(module, url, post=auth_payload)
    if axapi_failure(result):
        return module.fail_json(msg=result['response']['err']['msg'])
    signature = result['authresponse']['signature']
    return signature
