def wait_for_target_group(asg_connection, module, group_name):
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    wait_timeout = module.params.get('wait_timeout')
    as_group = asg_connection.describe_auto_scaling_groups(AutoScalingGroupNames=[group_name])['AutoScalingGroups'][0]
    if (as_group.get('TargetGroupARNs') and (as_group.get('HealthCheckType') == 'ELB')):
        log.debug('Waiting for Target Group to consider instances healthy.')
        elbv2_connection = boto3_conn(module, conn_type='client', resource='elbv2', region=region, endpoint=ec2_url, **aws_connect_params)
        wait_timeout = (time.time() + wait_timeout)
        healthy_instances = tg_healthy(asg_connection, elbv2_connection, module, group_name)
        while ((healthy_instances < as_group.get('MinSize')) and (wait_timeout > time.time())):
            healthy_instances = tg_healthy(asg_connection, elbv2_connection, module, group_name)
            log.debug('Target Group thinks {0} instances are healthy.'.format(healthy_instances))
            time.sleep(10)
        if (wait_timeout <= time.time()):
            module.fail_json(msg=('Waited too long for ELB instances to be healthy. %s' % time.asctime()))
        log.debug('Waiting complete. Target Group thinks {0} instances are healthy.'.format(healthy_instances))