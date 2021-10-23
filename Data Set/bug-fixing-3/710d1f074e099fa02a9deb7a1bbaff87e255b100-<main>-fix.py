def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(deregistration_delay_timeout=dict(type='int'), health_check_protocol=dict(choices=['http', 'https', 'tcp', 'HTTP', 'HTTPS', 'TCP'], type='str'), health_check_port=dict(), health_check_path=dict(default=None, type='str'), health_check_interval=dict(type='int'), health_check_timeout=dict(type='int'), healthy_threshold_count=dict(type='int'), modify_targets=dict(default=True, type='bool'), name=dict(required=True, type='str'), port=dict(type='int'), protocol=dict(choices=['http', 'https', 'tcp', 'HTTP', 'HTTPS', 'TCP'], type='str'), purge_tags=dict(default=True, type='bool'), stickiness_enabled=dict(type='bool'), stickiness_type=dict(default='lb_cookie', type='str'), stickiness_lb_cookie_duration=dict(type='int'), state=dict(required=True, choices=['present', 'absent'], type='str'), successful_response_codes=dict(type='str'), tags=dict(default={
        
    }, type='dict'), targets=dict(type='list'), unhealthy_threshold_count=dict(type='int'), vpc_id=dict(type='str'), wait_timeout=dict(type='int'), wait=dict(type='bool')))
    module = AnsibleModule(argument_spec=argument_spec, required_if=[('state', 'present', ['protocol', 'port', 'vpc_id'])])
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 required for this module')
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    if region:
        connection = boto3_conn(module, conn_type='client', resource='elbv2', region=region, endpoint=ec2_url, **aws_connect_params)
    else:
        module.fail_json(msg='region must be specified')
    state = module.params.get('state')
    if (state == 'present'):
        create_or_update_target_group(connection, module)
    else:
        delete_target_group(connection, module)