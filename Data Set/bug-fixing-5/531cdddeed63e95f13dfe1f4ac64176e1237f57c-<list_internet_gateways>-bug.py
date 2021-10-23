def list_internet_gateways(client, module):
    params = dict()
    params['Filters'] = ansible_dict_to_boto3_filter_list(module.params.get('filters'))
    if module.params.get('internet_gateway_ids'):
        params['InternetGatewayIds'] = module.params.get('internet_gateway_ids')
    try:
        all_internet_gateways = client.describe_internet_gateways(**params)
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=str(e))
    snaked_internet_gateways = [camel_dict_to_snake_dict(get_internet_gateway_info(igw)) for igw in all_internet_gateways['InternetGateways']]
    module.exit_json(internet_gateways=snaked_internet_gateways)