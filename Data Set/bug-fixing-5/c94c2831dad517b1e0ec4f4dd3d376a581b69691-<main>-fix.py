def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(bgp_asn=dict(required=False, type='int'), ip_address=dict(required=True), name=dict(required=True), state=dict(default='present', choices=['present', 'absent'])))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[('state', 'present', ['bgp_asn'])])
    if (not HAS_BOTOCORE):
        module.fail_json(msg='botocore is required.')
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 is required.')
    gw_mgr = Ec2CustomerGatewayManager(module)
    name = module.params.get('name')
    existing = gw_mgr.describe_gateways(module.params['ip_address'])
    results = dict(changed=False)
    if (module.params['state'] == 'present'):
        if existing['CustomerGateways']:
            existing['CustomerGateway'] = existing['CustomerGateways'][0]
            results['gateway'] = existing
            if existing['CustomerGateway']['Tags']:
                tag_array = existing['CustomerGateway']['Tags']
                for (key, value) in enumerate(tag_array):
                    if (value['Key'] == 'Name'):
                        current_name = value['Value']
                        if (current_name != name):
                            results['name'] = gw_mgr.tag_cgw_name(results['gateway']['CustomerGateway']['CustomerGatewayId'], module.params['name'])
                            results['changed'] = True
        else:
            if (not module.check_mode):
                results['gateway'] = gw_mgr.ensure_cgw_present(module.params['bgp_asn'], module.params['ip_address'])
                results['name'] = gw_mgr.tag_cgw_name(results['gateway']['CustomerGateway']['CustomerGatewayId'], module.params['name'])
            results['changed'] = True
    elif (module.params['state'] == 'absent'):
        if existing['CustomerGateways']:
            existing['CustomerGateway'] = existing['CustomerGateways'][0]
            results['gateway'] = existing
            if (not module.check_mode):
                results['gateway'] = gw_mgr.ensure_cgw_absent(existing['CustomerGateway']['CustomerGatewayId'])
            results['changed'] = True
    pretty_results = camel_dict_to_snake_dict(results)
    module.exit_json(**pretty_results)