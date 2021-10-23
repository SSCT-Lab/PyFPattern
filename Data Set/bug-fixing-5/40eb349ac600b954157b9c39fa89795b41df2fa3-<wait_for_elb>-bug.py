def wait_for_elb(asg_connection, module, group_name):
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    wait_timeout = module.params.get('wait_timeout')
    as_group = asg_connection.describe_auto_scaling_groups(AutoScalingGroupNames=[group_name])['AutoScalingGroups'][0]
    if (as_group.get('LoadBalancerNames') and (as_group.get('HealthCheckType') == 'ELB')):
        log.debug('Waiting for ELB to consider instances healthy.')
        elb_connection = boto3_conn(module, conn_type='client', resource='elb', region=region, endpoint=ec2_url, **aws_connect_params)
        wait_timeout = (time.time() + wait_timeout)
        healthy_instances = elb_healthy(asg_connection, elb_connection, module, group_name)
        while ((healthy_instances < as_group.get('MinSize')) and (wait_timeout > time.time())):
            healthy_instances = elb_healthy(asg_connection, elb_connection, module, group_name)
            log.debug('ELB thinks {0} instances are healthy.'.format(healthy_instances))
            time.sleep(10)
        if (wait_timeout <= time.time()):
            module.fail_json(msg=('Waited too long for ELB instances to be healthy. %s' % time.asctime()))
        log.debug('Waiting complete.  ELB thinks {0} instances are healthy.'.format(healthy_instances))