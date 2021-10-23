def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(name=dict(required=True, type='str'), load_balancers=dict(type='list'), target_group_arns=dict(type='list'), availability_zones=dict(type='list'), launch_config_name=dict(type='str'), min_size=dict(type='int'), max_size=dict(type='int'), placement_group=dict(type='str'), desired_capacity=dict(type='int'), vpc_zone_identifier=dict(type='list'), replace_batch_size=dict(type='int', default=1), replace_all_instances=dict(type='bool', default=False), replace_instances=dict(type='list', default=[]), lc_check=dict(type='bool', default=True), wait_timeout=dict(type='int', default=300), state=dict(default='present', choices=['present', 'absent']), tags=dict(type='list', default=[]), health_check_period=dict(type='int', default=300), health_check_type=dict(default='EC2', choices=['EC2', 'ELB']), default_cooldown=dict(type='int', default=300), wait_for_instances=dict(type='bool', default=True), termination_policies=dict(type='list', default='Default'), notification_topic=dict(type='str', default=None), notification_types=dict(type='list', default=['autoscaling:EC2_INSTANCE_LAUNCH', 'autoscaling:EC2_INSTANCE_LAUNCH_ERROR', 'autoscaling:EC2_INSTANCE_TERMINATE', 'autoscaling:EC2_INSTANCE_TERMINATE_ERROR']), suspend_processes=dict(type='list', default=[])))
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=[['replace_all_instances', 'replace_instances']])
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 required for this module')
    state = module.params.get('state')
    replace_instances = module.params.get('replace_instances')
    replace_all_instances = module.params.get('replace_all_instances')
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    try:
        connection = boto3_conn(module, conn_type='client', resource='autoscaling', region=region, endpoint=ec2_url, **aws_connect_params)
    except (botocore.exceptions.NoCredentialsError, botocore.exceptions.ProfileNotFound) as e:
        module.fail_json(msg="Can't authorize connection. Check your credentials and profile.", exceptions=traceback.format_exc(), **camel_dict_to_snake_dict(e.message))
    changed = create_changed = replace_changed = False
    if (state == 'present'):
        (create_changed, asg_properties) = create_autoscaling_group(connection, module)
    elif (state == 'absent'):
        changed = delete_autoscaling_group(connection, module)
        module.exit_json(changed=changed)
    if (replace_all_instances or replace_instances):
        (replace_changed, asg_properties) = replace(connection, module)
    if (create_changed or replace_changed):
        changed = True
    module.exit_json(changed=changed, **asg_properties)