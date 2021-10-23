def tg_healthy(asg_connection, elbv2_connection, module, group_name):
    healthy_instances = set()
    as_group = describe_autoscaling_groups(asg_connection, group_name)[0]
    props = get_properties(as_group, module)
    instances = []
    for (instance, settings) in props['instance_facts'].items():
        if ((settings['lifecycle_state'] == 'InService') and (settings['health_status'] == 'Healthy')):
            instances.append(dict(Id=instance))
    log.debug('ASG considers the following instances InService and Healthy: %s', instances)
    log.debug('Target Group instance status:')
    tg_instances = list()
    for tg in as_group.get('TargetGroupARNs'):
        try:
            tg_instances = describe_target_health(elbv2_connection, tg, instances)
        except botocore.exceptions.ClientError as e:
            if (e.response['Error']['Code'] == 'InvalidInstance'):
                return None
            module.fail_json(msg='Failed to get target group.', exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        except botocore.exceptions.BotoCoreError as e:
            module.fail_json(msg='Failed to get target group.', exception=traceback.format_exc())
        for i in tg_instances.get('TargetHealthDescriptions'):
            if (i['TargetHealth']['State'] == 'healthy'):
                healthy_instances.add(i['Target']['Id'])
            log.debug('Target Group Health State %s: %s', i['Target']['Id'], i['TargetHealth']['State'])
    return len(healthy_instances)