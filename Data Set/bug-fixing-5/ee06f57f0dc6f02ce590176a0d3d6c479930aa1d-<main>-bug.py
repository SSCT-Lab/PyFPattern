def main():
    rule_list_options = {
        'required': False,
        'type': 'list',
        'elements': 'list',
        'options': {
            'rule_number': dict(required=True, type='int'),
            'protocol': dict(required=True, choices=['tcp', 'udp', 'icmp', '-1', 'all']),
            'rule_action': dict(required=True, choices=['allow', 'deny']),
            'ipv4_cidr': dict(required=True),
            'icmp_type': dict(type='int'),
            'icmp_code': dict(type='int'),
            'from_port': dict(type='int'),
            'to_port': dict(type='int'),
        },
        'required_together': [('from_port', 'to_port'), ('icmp_type', 'icmp_code')],
        'mutually_exclusive': [('icmp_type', 'from_port')],
    }
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(vpc_id=dict(), name=dict(), nacl_id=dict(), subnets=dict(required=False, type='list', default=list()), tags=dict(required=False, type='dict'), ingress=rule_list_options, egress=rule_list_options, state=dict(default='present', choices=['present', 'absent'])))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_one_of=[['name', 'nacl_id']], required_if=[['state', 'present', ['vpc_id']]])
    if (not HAS_BOTO3):
        module.fail_json(msg='json, botocore and boto3 are required.')
    state = module.params.get('state').lower()
    try:
        (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
        client = boto3_conn(module, conn_type='client', resource='ec2', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except botocore.exceptions.NoCredentialsError as e:
        module.fail_json(msg=("Can't authorize connection - %s" % str(e)))
    invocations = {
        'present': setup_network_acl,
        'absent': remove_network_acl,
    }
    (changed, results) = invocations[state](client, module)
    module.exit_json(changed=changed, nacl_id=results)