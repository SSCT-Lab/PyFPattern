

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(instance_ids=dict(default=[], type='list'), filters=dict(default={
        
    }, type='dict')))
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=[['instance_ids', 'filters']], supports_check_mode=True)
    if (module._name == 'ec2_instance_facts'):
        module.deprecate("The 'ec2_instance_facts' module has been renamed to 'ec2_instance_info'", version='2.13')
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 required for this module')
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    if region:
        connection = boto3_conn(module, conn_type='client', resource='ec2', region=region, endpoint=ec2_url, **aws_connect_params)
    else:
        module.fail_json(msg='region must be specified')
    list_ec2_instances(connection, module)
