def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state=dict(required=True, choices=['present', 'absent'], type='str'), policy_name=dict(required=True, type='str'), service_namespace=dict(required=True, choices=['ecs', 'elasticmapreduce', 'ec2', 'appstream', 'dynamodb'], type='str'), resource_id=dict(required=True, type='str'), scalable_dimension=dict(required=True, choices=['ecs:service:DesiredCount', 'ec2:spot-fleet-request:TargetCapacity', 'elasticmapreduce:instancegroup:InstanceCount', 'appstream:fleet:DesiredCapacity', 'dynamodb:table:ReadCapacityUnits', 'dynamodb:table:WriteCapacityUnits', 'dynamodb:index:ReadCapacityUnits', 'dynamodb:index:WriteCapacityUnits'], type='str'), policy_type=dict(required=True, choices=['StepScaling', 'TargetTrackingScaling'], type='str'), step_scaling_policy_configuration=dict(required=False, type='dict'), target_tracking_scaling_policy_configuration=dict(required=False, type='dict')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 is required.')
    try:
        (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module, boto3=True)
        if (not region):
            module.fail_json(msg='Region must be specified as a parameter, in EC2_REGION or AWS_REGION environment variables or in boto configuration file')
        connection = boto3_conn(module, conn_type='client', resource='application-autoscaling', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except botocore.exceptions.ProfileNotFound as e:
        module.fail_json(msg=str(e))
    if (module.params.get('state') == 'present'):
        create_scaling_policy(connection, module)
    else:
        delete_scaling_policy(connection, module)