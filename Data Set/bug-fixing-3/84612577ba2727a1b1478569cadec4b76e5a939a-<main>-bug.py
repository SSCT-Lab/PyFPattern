def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(filters=dict(type='dict', default={
        
    }), dry_run=dict(type='bool', default=False, aliases=['DryRun']), dhcp_options_ids=dict(type='list', aliases=['DhcpOptionIds'])))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (module._name == 'ec2_vpc_dhcp_options_facts'):
        module.deprecate("The 'ec2_vpc_dhcp_options_facts' module has been renamed 'ec2_vpc_dhcp_option_facts' (option is no longer plural)", version=2.8)
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 and botocore are required.')
    try:
        (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
        connection = boto3_conn(module, conn_type='client', resource='ec2', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except botocore.exceptions.NoCredentialsError as e:
        module.fail_json(msg=("Can't authorize connection - " + str(e)))
    results = list_dhcp_options(connection, module)
    module.exit_json(result=results)