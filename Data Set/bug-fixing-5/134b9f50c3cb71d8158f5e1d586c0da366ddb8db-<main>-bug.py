def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(name=dict(required=True, type='str'), path=dict(default='/', type='str'), assume_role_policy_document=dict(type='json'), managed_policy=dict(type='list', aliases=['managed_policies']), state=dict(choices=['present', 'absent'], required=True), description=dict(required=False, type='str', default='')))
    module = AnsibleModule(argument_spec=argument_spec, required_if=[('state', 'present', ['assume_role_policy_document'])])
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 required for this module')
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    connection = boto3_conn(module, conn_type='client', resource='iam', region=region, endpoint=ec2_url, **aws_connect_params)
    state = module.params.get('state')
    if (state == 'present'):
        create_or_update_role(connection, module)
    else:
        destroy_role(connection, module)