

def create_or_update_target_group(connection, module):
    changed = False
    new_target_group = False
    params = dict()
    params['Name'] = module.params.get('name')
    params['Protocol'] = module.params.get('protocol').upper()
    params['Port'] = module.params.get('port')
    params['VpcId'] = module.params.get('vpc_id')
    tags = module.params.get('tags')
    purge_tags = module.params.get('purge_tags')
    deregistration_delay_timeout = module.params.get('deregistration_delay_timeout')
    stickiness_enabled = module.params.get('stickiness_enabled')
    stickiness_lb_cookie_duration = module.params.get('stickiness_lb_cookie_duration')
    stickiness_type = module.params.get('stickiness_type')
    if (module.params.get('health_check_path') is not None):
        params['HealthCheckPath'] = module.params.get('health_check_path')
        if (module.params.get('health_check_protocol') is not None):
            params['HealthCheckProtocol'] = module.params.get('health_check_protocol').upper()
        if (module.params.get('health_check_port') is not None):
            params['HealthCheckPort'] = module.params.get('health_check_port')
        if (module.params.get('health_check_interval') is not None):
            params['HealthCheckIntervalSeconds'] = module.params.get('health_check_interval')
        if (module.params.get('health_check_timeout') is not None):
            params['HealthCheckTimeoutSeconds'] = module.params.get('health_check_timeout')
        if (module.params.get('healthy_threshold_count') is not None):
            params['HealthyThresholdCount'] = module.params.get('healthy_threshold_count')
        if (module.params.get('unhealthy_threshold_count') is not None):
            params['UnhealthyThresholdCount'] = module.params.get('unhealthy_threshold_count')
        if (module.params.get('successful_response_codes') is not None):
            params['Matcher'] = {
                
            }
            params['Matcher']['HttpCode'] = module.params.get('successful_response_codes')
    if (module.params.get('target_type') is not None):
        params['TargetType'] = module.params.get('target_type')
        if (params['TargetType'] == 'ip'):
            fail_if_ip_target_type_not_supported(module)
    tg = get_target_group(connection, module)
    if tg:
        diffs = [param for param in ('Port', 'Protocol', 'VpcId') if (tg.get(param) != params.get(param))]
        if diffs:
            module.fail_json(msg=('Cannot modify %s parameter(s) for a target group' % ', '.join(diffs)))
        health_check_params = dict()
        if (module.params.get('health_check_path') is not None):
            if (('HealthCheckProtocol' in params) and (tg['HealthCheckProtocol'] != params['HealthCheckProtocol'])):
                health_check_params['HealthCheckProtocol'] = params['HealthCheckProtocol']
            if (('HealthCheckPort' in params) and (tg['HealthCheckPort'] != params['HealthCheckPort'])):
                health_check_params['HealthCheckPort'] = params['HealthCheckPort']
            if (('HealthCheckPath' in params) and (tg['HealthCheckPath'] != params['HealthCheckPath'])):
                health_check_params['HealthCheckPath'] = params['HealthCheckPath']
            if (('HealthCheckIntervalSeconds' in params) and (tg['HealthCheckIntervalSeconds'] != params['HealthCheckIntervalSeconds'])):
                health_check_params['HealthCheckIntervalSeconds'] = params['HealthCheckIntervalSeconds']
            if (('HealthCheckTimeoutSeconds' in params) and (tg['HealthCheckTimeoutSeconds'] != params['HealthCheckTimeoutSeconds'])):
                health_check_params['HealthCheckTimeoutSeconds'] = params['HealthCheckTimeoutSeconds']
            if (('HealthyThresholdCount' in params) and (tg['HealthyThresholdCount'] != params['HealthyThresholdCount'])):
                health_check_params['HealthyThresholdCount'] = params['HealthyThresholdCount']
            if (('UnhealthyThresholdCount' in params) and (tg['UnhealthyThresholdCount'] != params['UnhealthyThresholdCount'])):
                health_check_params['UnhealthyThresholdCount'] = params['UnhealthyThresholdCount']
            if ('Matcher' in params):
                current_matcher_list = tg['Matcher']['HttpCode'].split(',')
                requested_matcher_list = params['Matcher']['HttpCode'].split(',')
                if (set(current_matcher_list) != set(requested_matcher_list)):
                    health_check_params['Matcher'] = {
                        
                    }
                    health_check_params['Matcher']['HttpCode'] = ','.join(requested_matcher_list)
            try:
                if health_check_params:
                    connection.modify_target_group(TargetGroupArn=tg['TargetGroupArn'], **health_check_params)
                    changed = True
            except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                module.fail_json_aws(e, msg="Couldn't update target group")
        if module.params.get('modify_targets'):
            if module.params.get('targets'):
                params['Targets'] = module.params.get('targets')
                try:
                    current_targets = connection.describe_target_health(TargetGroupArn=tg['TargetGroupArn'])
                except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                    module.fail_json_aws(e, msg="Couldn't get target group health")
                current_instance_ids = []
                for instance in current_targets['TargetHealthDescriptions']:
                    current_instance_ids.append(instance['Target']['Id'])
                new_instance_ids = []
                for instance in params['Targets']:
                    new_instance_ids.append(instance['Id'])
                add_instances = (set(new_instance_ids) - set(current_instance_ids))
                if add_instances:
                    instances_to_add = []
                    for target in params['Targets']:
                        if (target['Id'] in add_instances):
                            instances_to_add.append({
                                'Id': target['Id'],
                                'Port': int(target.get('Port', module.params.get('port'))),
                            })
                    changed = True
                    try:
                        connection.register_targets(TargetGroupArn=tg['TargetGroupArn'], Targets=instances_to_add)
                    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                        module.fail_json_aws(e, msg="Couldn't register targets")
                    if module.params.get('wait'):
                        (status_achieved, registered_instances) = wait_for_status(connection, module, tg['TargetGroupArn'], instances_to_add, 'healthy')
                        if (not status_achieved):
                            module.fail_json(msg='Error waiting for target registration to be healthy - please check the AWS console')
                remove_instances = (set(current_instance_ids) - set(new_instance_ids))
                if remove_instances:
                    instances_to_remove = []
                    for target in current_targets['TargetHealthDescriptions']:
                        if (target['Target']['Id'] in remove_instances):
                            instances_to_remove.append({
                                'Id': target['Target']['Id'],
                                'Port': target['Target']['Port'],
                            })
                    changed = True
                    try:
                        connection.deregister_targets(TargetGroupArn=tg['TargetGroupArn'], Targets=instances_to_remove)
                    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                        module.fail_json_aws(e, msg="Couldn't remove targets")
                    if module.params.get('wait'):
                        (status_achieved, registered_instances) = wait_for_status(connection, module, tg['TargetGroupArn'], instances_to_remove, 'unused')
                        if (not status_achieved):
                            module.fail_json(msg='Error waiting for target deregistration - please check the AWS console')
            else:
                try:
                    current_targets = connection.describe_target_health(TargetGroupArn=tg['TargetGroupArn'])
                except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                    module.fail_json_aws(e, msg="Couldn't get target health")
                current_instances = current_targets['TargetHealthDescriptions']
                if current_instances:
                    instances_to_remove = []
                    for target in current_targets['TargetHealthDescriptions']:
                        instances_to_remove.append({
                            'Id': target['Target']['Id'],
                            'Port': target['Target']['Port'],
                        })
                    changed = True
                    try:
                        connection.deregister_targets(TargetGroupArn=tg['TargetGroupArn'], Targets=instances_to_remove)
                    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                        module.fail_json_aws(e, msg="Couldn't remove targets")
                    if module.params.get('wait'):
                        (status_achieved, registered_instances) = wait_for_status(connection, module, tg['TargetGroupArn'], instances_to_remove, 'unused')
                        if (not status_achieved):
                            module.fail_json(msg='Error waiting for target deregistration - please check the AWS console')
    else:
        try:
            connection.create_target_group(**params)
            changed = True
            new_target_group = True
        except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
            module.fail_json_aws(e, msg="Couldn't create target group")
        tg = get_target_group(connection, module)
        if module.params.get('targets'):
            params['Targets'] = module.params.get('targets')
            try:
                connection.register_targets(TargetGroupArn=tg['TargetGroupArn'], Targets=params['Targets'])
            except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                module.fail_json_aws(e, msg="Couldn't register targets")
            if module.params.get('wait'):
                (status_achieved, registered_instances) = wait_for_status(connection, module, tg['TargetGroupArn'], params['Targets'], 'healthy')
                if (not status_achieved):
                    module.fail_json(msg='Error waiting for target registration to be healthy - please check the AWS console')
    update_attributes = []
    current_tg_attributes = get_tg_attributes(connection, module, tg['TargetGroupArn'])
    if (deregistration_delay_timeout is not None):
        if (str(deregistration_delay_timeout) != current_tg_attributes['deregistration_delay_timeout_seconds']):
            update_attributes.append({
                'Key': 'deregistration_delay.timeout_seconds',
                'Value': str(deregistration_delay_timeout),
            })
    if (stickiness_enabled is not None):
        if (stickiness_enabled and (current_tg_attributes['stickiness_enabled'] != 'true')):
            update_attributes.append({
                'Key': 'stickiness.enabled',
                'Value': 'true',
            })
    if (stickiness_lb_cookie_duration is not None):
        if (str(stickiness_lb_cookie_duration) != current_tg_attributes['stickiness_lb_cookie_duration_seconds']):
            update_attributes.append({
                'Key': 'stickiness.lb_cookie.duration_seconds',
                'Value': str(stickiness_lb_cookie_duration),
            })
    if ((stickiness_type is not None) and ('stickiness_type' in current_tg_attributes)):
        if (stickiness_type != current_tg_attributes['stickiness_type']):
            update_attributes.append({
                'Key': 'stickiness.type',
                'Value': stickiness_type,
            })
    if update_attributes:
        try:
            connection.modify_target_group_attributes(TargetGroupArn=tg['TargetGroupArn'], Attributes=update_attributes)
            changed = True
        except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
            if new_target_group:
                connection.delete_target_group(TargetGroupArn=tg['TargetGroupArn'])
            module.fail_json_aws(e, msg="Couldn't delete target group")
    if tags:
        current_tags = get_target_group_tags(connection, module, tg['TargetGroupArn'])
        (tags_need_modify, tags_to_delete) = compare_aws_tags(boto3_tag_list_to_ansible_dict(current_tags), tags, purge_tags)
        if tags_to_delete:
            try:
                connection.remove_tags(ResourceArns=[tg['TargetGroupArn']], TagKeys=tags_to_delete)
            except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                module.fail_json_aws(e, msg="Couldn't delete tags from target group")
            changed = True
        if tags_need_modify:
            try:
                connection.add_tags(ResourceArns=[tg['TargetGroupArn']], Tags=ansible_dict_to_boto3_tag_list(tags_need_modify))
            except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                module.fail_json_aws(e, msg="Couldn't add tags to target group")
            changed = True
    tg = get_target_group(connection, module)
    tg.update(get_tg_attributes(connection, module, tg['TargetGroupArn']))
    snaked_tg = camel_dict_to_snake_dict(tg)
    snaked_tg['tags'] = boto3_tag_list_to_ansible_dict(get_target_group_tags(connection, module, tg['TargetGroupArn']))
    module.exit_json(changed=changed, **snaked_tg)
