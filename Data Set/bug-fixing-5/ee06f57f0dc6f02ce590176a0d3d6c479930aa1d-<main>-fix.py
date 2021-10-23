def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(vpc_id=dict(), name=dict(), nacl_id=dict(), subnets=dict(required=False, type='list', default=list()), tags=dict(required=False, type='dict'), ingress=dict(required=False, type='list', default=list()), egress=dict(required=False, type='list', default=list()), state=dict(default='present', choices=['present', 'absent'])))
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