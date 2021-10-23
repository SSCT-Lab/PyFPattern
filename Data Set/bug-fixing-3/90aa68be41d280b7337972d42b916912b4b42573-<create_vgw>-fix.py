def create_vgw(client, module):
    params = dict()
    params['Type'] = module.params.get('type')
    if module.params.get('asn'):
        params['AmazonSideAsn'] = module.params.get('asn')
    try:
        response = client.create_vpn_gateway(**params)
        get_waiter(client, 'vpn_gateway_exists').wait(VpnGatewayIds=[response['VpnGateway']['VpnGatewayId']])
    except botocore.exceptions.WaiterError as e:
        module.fail_json(msg='Failed to wait for Vpn Gateway {0} to be available'.format(response['VpnGateway']['VpnGatewayId']), exception=traceback.format_exc())
    except client.exceptions.from_code('VpnGatewayLimitExceeded') as e:
        module.fail_json(msg='Too many VPN gateways exist in this account.', exception=traceback.format_exc())
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())
    result = response
    return result