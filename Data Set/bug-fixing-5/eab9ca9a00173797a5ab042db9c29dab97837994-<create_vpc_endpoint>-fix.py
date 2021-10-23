def create_vpc_endpoint(client, module):
    params = dict()
    changed = False
    token_provided = False
    params['VpcId'] = module.params.get('vpc_id')
    params['ServiceName'] = module.params.get('service')
    params['DryRun'] = module.check_mode
    if module.params.get('route_table_ids'):
        params['RouteTableIds'] = module.params.get('route_table_ids')
    if module.params.get('client_token'):
        token_provided = True
        request_time = datetime.datetime.utcnow()
        params['ClientToken'] = module.params.get('client_token')
    policy = None
    if module.params.get('policy'):
        try:
            policy = json.loads(module.params.get('policy'))
        except ValueError as e:
            module.fail_json(msg=str(e), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    elif module.params.get('policy_file'):
        try:
            with open(module.params.get('policy_file'), 'r') as json_data:
                policy = json.load(json_data)
        except Exception as e:
            module.fail_json(msg=str(e), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    if policy:
        params['PolicyDocument'] = json.dumps(policy)
    try:
        changed = True
        result = camel_dict_to_snake_dict(client.create_vpc_endpoint(**params)['VpcEndpoint'])
        if (token_provided and (request_time > result['creation_timestamp'].replace(tzinfo=None))):
            changed = False
        elif (module.params.get('wait') and (not module.check_mode)):
            (status_achieved, result) = wait_for_status(client, module, result['vpc_endpoint_id'], 'available')
            if (not status_achieved):
                module.fail_json(msg='Error waiting for vpc endpoint to become available - please check the AWS console')
    except botocore.exceptions.ClientError as e:
        if ('DryRunOperation' in e.message):
            changed = True
            result = 'Would have created VPC Endpoint if not in check mode'
        elif ('IdempotentParameterMismatch' in e.message):
            module.fail_json(msg='IdempotentParameterMismatch - updates of endpoints are not allowed by the API')
        elif ('RouteAlreadyExists' in e.message):
            module.fail_json(msg='RouteAlreadyExists for one of the route tables - update is not allowed by the API')
        else:
            module.fail_json(msg=str(e), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    return (changed, result)