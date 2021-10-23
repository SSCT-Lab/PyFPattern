def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(name=dict(required=True, type='str'), managed_policy=dict(default=[], type='list'), state=dict(choices=['present', 'absent'], required=True), purge_policy=dict(default=False, type='bool')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 required for this module')
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    connection = boto3_conn(module, conn_type='client', resource='iam', region=region, endpoint=ec2_url, **aws_connect_params)
    state = module.params.get('state')
    if (state == 'present'):
        create_or_update_user(connection, module)
    else:
        destroy_user(connection, module)