def create_or_update_elb(connection, connection_ec2, module):
    'Create ELB or modify main attributes. json_exit here'
    changed = False
    new_load_balancer = False
    params = dict()
    params['Name'] = module.params.get('name')
    params['Subnets'] = module.params.get('subnets')
    try:
        params['SecurityGroups'] = get_ec2_security_group_ids_from_names(module.params.get('security_groups'), connection_ec2, boto3=True)
    except ValueError as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    except ClientError as e:
        module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    except NoCredentialsError as e:
        module.fail_json(msg=('AWS authentication problem. ' + e.message), exception=traceback.format_exc())
    params['Scheme'] = module.params.get('scheme')
    if module.params.get('tags'):
        params['Tags'] = ansible_dict_to_boto3_tag_list(module.params.get('tags'))
    purge_tags = module.params.get('purge_tags')
    access_logs_enabled = module.params.get('access_logs_enabled')
    access_logs_s3_bucket = module.params.get('access_logs_s3_bucket')
    access_logs_s3_prefix = module.params.get('access_logs_s3_prefix')
    deletion_protection = module.params.get('deletion_protection')
    idle_timeout = module.params.get('idle_timeout')
    elb = get_elb(connection, module)
    if elb:
        if (set(_get_subnet_ids_from_subnet_list(elb['AvailabilityZones'])) != set(params['Subnets'])):
            try:
                connection.set_subnets(LoadBalancerArn=elb['LoadBalancerArn'], Subnets=params['Subnets'])
            except ClientError as e:
                module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
            changed = True
        if (set(elb['SecurityGroups']) != set(params['SecurityGroups'])):
            try:
                connection.set_security_groups(LoadBalancerArn=elb['LoadBalancerArn'], SecurityGroups=params['SecurityGroups'])
            except ClientError as e:
                module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
            changed = True
        if module.params.get('tags'):
            try:
                elb_tags = connection.describe_tags(ResourceArns=[elb['LoadBalancerArn']])['TagDescriptions'][0]['Tags']
            except ClientError as e:
                module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
            (tags_need_modify, tags_to_delete) = compare_aws_tags(boto3_tag_list_to_ansible_dict(elb_tags), boto3_tag_list_to_ansible_dict(params['Tags']), purge_tags)
            if tags_to_delete:
                try:
                    connection.remove_tags(ResourceArns=[elb['LoadBalancerArn']], TagKeys=tags_to_delete)
                except ClientError as e:
                    module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
                changed = True
            if tags_need_modify:
                try:
                    connection.add_tags(ResourceArns=[elb['LoadBalancerArn']], Tags=params['Tags'])
                except ClientError as e:
                    module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
                changed = True
    else:
        try:
            elb = connection.create_load_balancer(**params)['LoadBalancers'][0]
            changed = True
            new_load_balancer = True
        except ClientError as e:
            module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        if module.params.get('wait'):
            (status_achieved, new_elb) = wait_for_status(connection, module, elb['LoadBalancerArn'], 'active')
    update_attributes = []
    current_elb_attributes = get_elb_attributes(connection, module, elb['LoadBalancerArn'])
    if (access_logs_enabled and (current_elb_attributes['access_logs_s3_enabled'] != 'true')):
        update_attributes.append({
            'Key': 'access_logs.s3.enabled',
            'Value': 'true',
        })
    if ((not access_logs_enabled) and (current_elb_attributes['access_logs_s3_enabled'] != 'false')):
        update_attributes.append({
            'Key': 'access_logs.s3.enabled',
            'Value': 'false',
        })
    if ((access_logs_s3_bucket is not None) and (access_logs_s3_bucket != current_elb_attributes['access_logs_s3_bucket'])):
        update_attributes.append({
            'Key': 'access_logs.s3.bucket',
            'Value': access_logs_s3_bucket,
        })
    if ((access_logs_s3_prefix is not None) and (access_logs_s3_prefix != current_elb_attributes['access_logs_s3_prefix'])):
        update_attributes.append({
            'Key': 'access_logs.s3.prefix',
            'Value': access_logs_s3_prefix,
        })
    if (deletion_protection and (current_elb_attributes['deletion_protection_enabled'] != 'true')):
        update_attributes.append({
            'Key': 'deletion_protection.enabled',
            'Value': 'true',
        })
    if ((not deletion_protection) and (current_elb_attributes['deletion_protection_enabled'] != 'false')):
        update_attributes.append({
            'Key': 'deletion_protection.enabled',
            'Value': 'false',
        })
    if ((idle_timeout is not None) and (str(idle_timeout) != current_elb_attributes['idle_timeout_timeout_seconds'])):
        update_attributes.append({
            'Key': 'idle_timeout.timeout_seconds',
            'Value': str(idle_timeout),
        })
    if update_attributes:
        try:
            connection.modify_load_balancer_attributes(LoadBalancerArn=elb['LoadBalancerArn'], Attributes=update_attributes)
            changed = True
        except ClientError as e:
            if new_load_balancer:
                connection.delete_load_balancer(LoadBalancerArn=elb['LoadBalancerArn'])
            module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    try:
        listener_changed = create_or_update_elb_listeners(connection, module, elb)
        if listener_changed:
            changed = True
    except ClientError as e:
        if new_load_balancer:
            connection.delete_load_balancer(LoadBalancerArn=elb['LoadBalancerArn'])
        module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    elb = get_elb(connection, module)
    elb['listeners'] = get_elb_listeners(connection, module, elb['LoadBalancerArn'])
    for listener in elb['listeners']:
        listener['rules'] = get_listener_rules(connection, module, listener['ListenerArn'])
    elb.update(get_elb_attributes(connection, module, elb['LoadBalancerArn']))
    snaked_elb = camel_dict_to_snake_dict(elb)
    elb_tags = connection.describe_tags(ResourceArns=[elb['LoadBalancerArn']])['TagDescriptions'][0]['Tags']
    snaked_elb['tags'] = boto3_tag_list_to_ansible_dict(elb_tags)
    module.exit_json(changed=changed, **snaked_elb)