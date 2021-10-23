

def get_nat_gateways(client, module, nat_gateway_id=None):
    params = dict()
    params['Filter'] = ansible_dict_to_boto3_filter_list(module.params.get('filters'))
    params['NatGatewayIds'] = module.params.get('nat_gateway_ids')
    try:
        result = json.loads(json.dumps(client.describe_nat_gateways(**params), default=date_handler))
    except Exception as e:
        module.fail_json(msg=str(e.message))
    return result['NatGateways']
