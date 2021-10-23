def create_update_parameter(client, module):
    changed = False
    response = {
        
    }
    args = dict(Name=module.params.get('name'), Value=module.params.get('value'), Type=module.params.get('string_type'), Overwrite=module.params.get('overwrite'))
    if module.params.get('description'):
        args.update(Description=module.params.get('description'))
    if (module.params.get('string_type') == 'SecureString'):
        args.update(KeyId=module.params.get('key_id'))
    try:
        response = client.put_parameter(**args)
        changed = True
    except ClientError as e:
        module.fail_json_aws(e, msg='setting parameter')
    return (changed, response)