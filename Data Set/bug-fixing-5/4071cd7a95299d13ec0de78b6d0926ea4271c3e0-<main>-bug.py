def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(names=dict(type='list', default=[])))
    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 and botocore are required for this module')
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    connection = boto3_conn(module, resource='ec2', conn_type='client', region=region, **aws_connect_params)
    placement_groups = get_placement_groups_details(connection, module)
    module.exit_json(changed=False, placement_groups=placement_groups)