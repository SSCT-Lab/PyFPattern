

def create_update_parameter(client, module):
    changed = False
    existing_parameter = None
    response = {
        
    }
    args = dict(Name=module.params.get('name'), Value=module.params.get('value'), Type=module.params.get('string_type'))
    if (module.params.get('overwrite_value') in ('always', 'changed')):
        args.update(Overwrite=True)
    else:
        args.update(Overwrite=False)
    if module.params.get('description'):
        args.update(Description=module.params.get('description'))
    if (module.params.get('string_type') == 'SecureString'):
        args.update(KeyId=module.params.get('key_id'))
    try:
        existing_parameter = client.get_parameter(Name=args['Name'], WithDecryption=True)
    except:
        pass
    if existing_parameter:
        if (module.params.get('overwrite_value') == 'always'):
            (changed, response) = update_parameter(client, module, args)
        elif (module.params.get('overwrite_value') == 'changed'):
            if (existing_parameter['Parameter']['Type'] != args['Type']):
                (changed, response) = update_parameter(client, module, args)
            if (existing_parameter['Parameter']['Value'] != args['Value']):
                (changed, response) = update_parameter(client, module, args)
            if args.get('Description'):
                describe_existing_parameter = None
                try:
                    describe_existing_parameter = client.describe_parameters(Filters=[{
                        'Key': 'Name',
                        'Values': [args['Name']],
                    }])
                except ClientError as e:
                    module.fail_json_aws(e, msg='getting description value')
                if (describe_existing_parameter['Parameters'][0]['Description'] != args['Description']):
                    (changed, response) = update_parameter(client, module, args)
    else:
        (changed, response) = update_parameter(client, module, args)
    return (changed, response)
