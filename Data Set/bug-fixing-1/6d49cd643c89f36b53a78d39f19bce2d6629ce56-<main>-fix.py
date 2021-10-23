

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state=dict(required=True, choices=['present', 'absent'], type='str'), policy_name=dict(required=True, type='str'), service_namespace=dict(required=True, choices=['ecs', 'elasticmapreduce', 'ec2', 'appstream', 'dynamodb'], type='str'), resource_id=dict(required=True, type='str'), scalable_dimension=dict(required=True, choices=['ecs:service:DesiredCount', 'ec2:spot-fleet-request:TargetCapacity', 'elasticmapreduce:instancegroup:InstanceCount', 'appstream:fleet:DesiredCapacity', 'dynamodb:table:ReadCapacityUnits', 'dynamodb:table:WriteCapacityUnits', 'dynamodb:index:ReadCapacityUnits', 'dynamodb:index:WriteCapacityUnits'], type='str'), policy_type=dict(required=True, choices=['StepScaling', 'TargetTrackingScaling'], type='str'), step_scaling_policy_configuration=dict(required=False, type='dict'), target_tracking_scaling_policy_configuration=dict(required=False, type='dict', options=dict(CustomizedMetricSpecification=dict(type='dict'), DisableScaleIn=dict(type='bool'), PredefinedMetricSpecification=dict(type='dict'), ScaleInCooldown=dict(type='int'), ScaleOutCooldown=dict(type='int'), TargetValue=dict(type='float'))), minimum_tasks=dict(required=False, type='int'), maximum_tasks=dict(required=False, type='int'), override_task_capacity=dict(required=False, type=bool)))
    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True)
    connection = module.client('application-autoscaling')
    policy_config_options = ['CustomizedMetricSpecification', 'DisableScaleIn', 'PredefinedMetricSpecification', 'ScaleInCooldown', 'ScaleOutCooldown', 'TargetValue']
    if isinstance(module.params['target_tracking_scaling_policy_configuration'], dict):
        for option in policy_config_options:
            if (module.params['target_tracking_scaling_policy_configuration'][option] is None):
                module.params['target_tracking_scaling_policy_configuration'].pop(option)
    if (module.params.get('state') == 'present'):
        scalable_target_result = create_scalable_target(connection, module)
        policy_result = create_scaling_policy(connection, module)
        merged_result = merge_results(scalable_target_result, policy_result)
        module.exit_json(**merged_result)
    else:
        policy_result = delete_scaling_policy(connection, module)
        module.exit_json(**policy_result)
