def get_properties(autoscaling_group, module):
    properties = dict()
    properties['healthy_instances'] = 0
    properties['in_service_instances'] = 0
    properties['unhealthy_instances'] = 0
    properties['pending_instances'] = 0
    properties['viable_instances'] = 0
    properties['terminating_instances'] = 0
    instance_facts = dict()
    autoscaling_group_instances = autoscaling_group.get('Instances')
    if autoscaling_group_instances:
        properties['instances'] = [i['InstanceId'] for i in autoscaling_group_instances]
        for i in autoscaling_group_instances:
            instance_facts[i['InstanceId']] = {
                'health_status': i['HealthStatus'],
                'lifecycle_state': i['LifecycleState'],
                'launch_config_name': i.get('LaunchConfigurationName'),
            }
            if ((i['HealthStatus'] == 'Healthy') and (i['LifecycleState'] == 'InService')):
                properties['viable_instances'] += 1
            if (i['HealthStatus'] == 'Healthy'):
                properties['healthy_instances'] += 1
            else:
                properties['unhealthy_instances'] += 1
            if (i['LifecycleState'] == 'InService'):
                properties['in_service_instances'] += 1
            if (i['LifecycleState'] == 'Terminating'):
                properties['terminating_instances'] += 1
            if (i['LifecycleState'] == 'Pending'):
                properties['pending_instances'] += 1
    else:
        properties['instances'] = []
    properties['instance_facts'] = instance_facts
    properties['load_balancers'] = autoscaling_group.get('LoadBalancerNames')
    properties['launch_config_name'] = autoscaling_group.get('LaunchConfigurationName')
    properties['tags'] = autoscaling_group.get('Tags')
    properties['min_size'] = autoscaling_group.get('MinSize')
    properties['max_size'] = autoscaling_group.get('MaxSize')
    properties['desired_capacity'] = autoscaling_group.get('DesiredCapacity')
    properties['default_cooldown'] = autoscaling_group.get('DefaultCooldown')
    properties['healthcheck_grace_period'] = autoscaling_group.get('HealthCheckGracePeriod')
    properties['healthcheck_type'] = autoscaling_group.get('HealthCheckType')
    properties['default_cooldown'] = autoscaling_group.get('DefaultCooldown')
    properties['termination_policies'] = autoscaling_group.get('TerminationPolicies')
    properties['target_group_arns'] = autoscaling_group.get('TargetGroupARNs')
    if properties['target_group_arns']:
        (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
        elbv2_connection = boto3_conn(module, conn_type='client', resource='elbv2', region=region, endpoint=ec2_url, **aws_connect_params)
        tg_paginator = elbv2_connection.get_paginator('describe_target_groups')
        tg_result = tg_paginator.paginate(TargetGroupArns=properties['target_group_arns']).build_full_result()
        target_groups = tg_result['TargetGroups']
    else:
        target_groups = []
    properties['target_group_names'] = [tg['TargetGroupName'] for tg in target_groups]
    return properties