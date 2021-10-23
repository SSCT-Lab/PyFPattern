def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(access_logs_enabled=dict(type='bool'), access_logs_s3_bucket=dict(type='str'), access_logs_s3_prefix=dict(type='str'), deletion_protection=dict(default=False, type='bool'), idle_timeout=dict(type='int'), listeners=dict(type='list'), name=dict(required=True, type='str'), purge_listeners=dict(default=True, type='bool'), purge_tags=dict(default=True, type='bool'), subnets=dict(type='list'), security_groups=dict(type='list'), scheme=dict(default='internet-facing', choices=['internet-facing', 'internal']), state=dict(choices=['present', 'absent'], type='str'), tags=dict(default={
        
    }, type='dict'), type=dict(default='application', type='str', choices=['application', 'network']), wait_timeout=dict(type='int'), wait=dict(type='bool')))
    module = AnsibleModule(argument_spec=argument_spec, required_if=[('state', 'present', ['subnets'])], required_together=['access_logs_enabled', 'access_logs_s3_bucket', 'access_logs_s3_prefix'])
    listeners = module.params.get('listeners')
    if (listeners is not None):
        for listener in listeners:
            for key in listener.keys():
                if (key not in ['Protocol', 'Port', 'SslPolicy', 'Certificates', 'DefaultActions', 'Rules']):
                    module.fail_json(msg="listeners parameter contains invalid dict keys. Should be one of 'Protocol', 'Port', 'SslPolicy', 'Certificates', 'DefaultActions', 'Rules'.")
                elif (key == 'Port'):
                    listener[key] = int(listener[key])
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