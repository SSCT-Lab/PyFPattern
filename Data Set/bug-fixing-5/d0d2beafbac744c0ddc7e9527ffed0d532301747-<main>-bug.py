def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(access_logs_enabled=dict(required=False, type='bool'), access_logs_s3_bucket=dict(required=False, type='str'), access_logs_s3_prefix=dict(required=False, type='str'), deletion_protection=dict(required=False, default=False, type='bool'), idle_timeout=dict(required=False, type='int'), listeners=dict(required=False, type='list'), name=dict(required=True, type='str'), purge_tags=dict(required=False, default=True, type='bool'), subnets=dict(required=False, type='list'), security_groups=dict(required=False, type='list'), scheme=dict(required=False, default='internet-facing', choices=['internet-facing', 'internal']), state=dict(required=True, choices=['present', 'absent'], type='str'), tags=dict(required=False, default={
        
    }, type='dict'), wait_timeout=dict(required=False, type='int'), wait=dict(required=False, type='bool')))
    module = AnsibleModule(argument_spec=argument_spec, required_if=[('state', 'present', ['subnets', 'security_groups'])], required_together=['access_logs_enabled', 'access_logs_s3_bucket', 'access_logs_s3_prefix'])
    listeners = module.params.get('listeners')
    if (listeners is not None):
        for listener in listeners:
            for key in listener.keys():
                if (key not in ['Protocol', 'Port', 'SslPolicy', 'Certificates', 'DefaultActions', 'Rules']):
                    module.fail_json(msg="listeners parameter contains invalid dict keys. Should be one of 'Protocol', 'Port', 'SslPolicy', 'Certificates', 'DefaultActions', 'Rules'.")
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 required for this module')
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    if region:
        connection = boto3_conn(module, conn_type='client', resource='elbv2', region=region, endpoint=ec2_url, **aws_connect_params)
        connection_ec2 = boto3_conn(module, conn_type='client', resource='ec2', region=region, endpoint=ec2_url, **aws_connect_params)
    else:
        module.fail_json(msg='region must be specified')
    state = module.params.get('state')
    if (state == 'present'):
        create_or_update_elb(connection, connection_ec2, module)
    else:
        delete_elb(connection, module)