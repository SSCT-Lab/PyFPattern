def elb_dreg(asg_connection, module, group_name, instance_id):
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module, boto3=True)
    as_group = describe_autoscaling_groups(asg_connection, group_name)[0]
    wait_timeout = module.params.get('wait_timeout')
    count = 1
    if (as_group['LoadBalancerNames'] and (as_group['HealthCheckType'] == 'ELB')):
        elb_connection = boto3_conn(module, conn_type='client', resource='elb', region=region, endpoint=ec2_url, **aws_connect_params)
    else:
        return
    for lb in as_group['LoadBalancerNames']:
        deregister_lb_instances(elb_connection, lb, instance_id)
        log.debug('De-registering %s from ELB %s', instance_id, lb)
    wait_timeout = (time.time() + wait_timeout)
    while ((wait_timeout > time.time()) and (count > 0)):
        count = 0
        for lb in as_group['LoadBalancerNames']:
            lb_instances = describe_instance_health(elb_connection, lb, [])
            for i in lb_instances['InstanceStates']:
                if ((i['InstanceId'] == instance_id) and (i['State'] == 'InService')):
                    count += 1
                    log.debug('%s: %s, %s', i['InstanceId'], i['State'], i['Description'])
        time.sleep(10)
    if (wait_timeout <= time.time()):
        module.fail_json(msg='Waited too long for instance to deregister. {0}'.format(time.asctime()))