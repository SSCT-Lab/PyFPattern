def elb_healthy(asg_connection, elb_connection, module, group_name):
    healthy_instances = set()
    as_group = asg_connection.describe_auto_scaling_groups(AutoScalingGroupNames=[group_name])['AutoScalingGroups'][0]
    props = get_properties(as_group)
    instances = []
    for (instance, settings) in props['instance_facts'].items():
        if ((settings['lifecycle_state'] == 'InService') and (settings['health_status'] == 'Healthy')):
            instances.append(dict(InstanceId=instance))
    log.debug('ASG considers the following instances InService and Healthy: {0}'.format(instances))
    log.debug('ELB instance status:')
    lb_instances = list()
    for lb in as_group.get('LoadBalancerNames'):
        try:
            lb_instances = elb_connection.describe_instance_health(LoadBalancerName=lb, Instances=instances)
        except botocore.exceptions.ClientError as e:
            if (e.response['Error']['Code'] == 'InvalidInstance'):
                return None
            module.fail_json(msg='Failed to get load balancer.', exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        except botocore.exceptions.BotoCoreError as e:
            module.fail_json(msg='Failed to get load balancer.', exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.message))
        for i in lb_instances.get('InstanceStates'):
            if (i['State'] == 'InService'):
                healthy_instances.add(i['InstanceId'])
            log.debug('ELB Health State {0}: {1}'.format(i['InstanceId'], i['State']))
    return len(healthy_instances)