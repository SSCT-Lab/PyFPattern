def elb_dreg(asg_connection, module, group_name, instance_id):
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    as_group = asg_connection.describe_auto_scaling_groups(AutoScalingGroupNames=[group_name])['AutoScalingGroups'][0]
    wait_timeout = module.params.get('wait_timeout')
    count = 1
    if (as_group['LoadBalancerNames'] and (as_group['HealthCheckType'] == 'ELB')):
        elb_connection = boto3_conn(module, conn_type='client', resource='elb', region=region, endpoint=ec2_url, **aws_connect_params)
    else:
        return
    for lb in as_group['LoadBalancerNames']:
        elb_connection.deregister_instances_from_load_balancer(LoadBalancerName=lb, Instances=[dict(InstanceId=instance_id)])
        log.debug('De-registering {0} from ELB {1}'.format(instance_id, lb))
    wait_timeout = (time.time() + wait_timeout)
    while ((wait_timeout > time.time()) and (count > 0)):
        count = 0
        for lb in as_group['LoadBalancerNames']:
            lb_instances = elb_connection.describe_instance_health(LoadBalancerName=lb)
            for i in lb_instances['InstanceStates']:
                if ((i['InstanceId'] == instance_id) and (i['State'] == 'InService')):
                    count += 1
                    log.debug('{0}: {1}, {2}'.format(i['InstanceId'], i['State'], i['Description']))
        time.sleep(10)
    if (wait_timeout <= time.time()):
        module.fail_json(msg='Waited too long for instance to deregister. {0}'.format(time.asctime()))