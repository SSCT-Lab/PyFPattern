def list_virtual_gateways(client, module):
    params = dict()
    params['Filters'] = ansible_dict_to_boto3_filter_list(module.params.get('filters'))
    params['DryRun'] = module.check_mode
    if module.params.get('vpn_gateway_ids'):
        params['VpnGatewayIds'] = module.params.get('vpn_gateway_ids')
    try:
        all_virtual_gateways = client.describe_vpn_gateways(**params)
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    return [camel_dict_to_snake_dict(get_virtual_gateway_info(vgw)) for vgw in all_virtual_gateways['VpnGateways']]