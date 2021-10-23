

def create_autoscaling_group(connection, module):
    group_name = module.params.get('name')
    load_balancers = module.params['load_balancers']
    availability_zones = module.params['availability_zones']
    launch_config_name = module.params.get('launch_config_name')
    min_size = module.params['min_size']
    max_size = module.params['max_size']
    placement_group = module.params.get('placement_group')
    desired_capacity = module.params.get('desired_capacity')
    vpc_zone_identifier = module.params.get('vpc_zone_identifier')
    set_tags = module.params.get('tags')
    health_check_period = module.params.get('health_check_period')
    health_check_type = module.params.get('health_check_type')
    default_cooldown = module.params.get('default_cooldown')
    wait_for_instances = module.params.get('wait_for_instances')
    as_groups = connection.get_all_groups(names=[group_name])
    wait_timeout = module.params.get('wait_timeout')
    termination_policies = module.params.get('termination_policies')
    notification_topic = module.params.get('notification_topic')
    notification_types = module.params.get('notification_types')
    if ((not vpc_zone_identifier) and (not availability_zones)):
        (region, ec2_url, aws_connect_params) = get_aws_connection_info(module)
        try:
            ec2_connection = connect_to_aws(boto.ec2, region, **aws_connect_params)
        except (boto.exception.NoAuthHandlerFound, AnsibleAWSError) as e:
            module.fail_json(msg=str(e))
    elif vpc_zone_identifier:
        vpc_zone_identifier = ','.join(vpc_zone_identifier)
    asg_tags = []
    for tag in set_tags:
        for (k, v) in tag.items():
            if (k != 'propagate_at_launch'):
                asg_tags.append(Tag(key=k, value=v, propagate_at_launch=bool(tag.get('propagate_at_launch', True)), resource_id=group_name))
    if (not as_groups):
        if ((not vpc_zone_identifier) and (not availability_zones)):
            availability_zones = module.params['availability_zones'] = [zone.name for zone in ec2_connection.get_all_zones()]
        enforce_required_arguments(module)
        launch_configs = connection.get_all_launch_configurations(names=[launch_config_name])
        if (len(launch_configs) == 0):
            module.fail_json(msg=('No launch config found with name %s' % launch_config_name))
        ag = AutoScalingGroup(group_name=group_name, load_balancers=load_balancers, availability_zones=availability_zones, launch_config=launch_configs[0], min_size=min_size, max_size=max_size, placement_group=placement_group, desired_capacity=desired_capacity, vpc_zone_identifier=vpc_zone_identifier, connection=connection, tags=asg_tags, health_check_period=health_check_period, health_check_type=health_check_type, default_cooldown=default_cooldown, termination_policies=termination_policies)
        try:
            connection.create_auto_scaling_group(ag)
            suspend_processes(ag, module)
            if wait_for_instances:
                wait_for_new_inst(module, connection, group_name, wait_timeout, desired_capacity, 'viable_instances')
                wait_for_elb(connection, module, group_name)
            if notification_topic:
                ag.put_notification_configuration(notification_topic, notification_types)
            as_group = connection.get_all_groups(names=[group_name])[0]
            asg_properties = get_properties(as_group)
            changed = True
            return (changed, asg_properties)
        except BotoServerError as e:
            module.fail_json(msg=('Failed to create Autoscaling Group: %s' % str(e)), exception=traceback.format_exc())
    else:
        as_group = as_groups[0]
        changed = False
        if suspend_processes(as_group, module):
            changed = True
        for attr in ASG_ATTRIBUTES:
            if (module.params.get(attr, None) is not None):
                module_attr = module.params.get(attr)
                if (attr == 'vpc_zone_identifier'):
                    module_attr = ','.join(module_attr)
                group_attr = getattr(as_group, attr)
                if (attr != 'termination_policies'):
                    try:
                        module_attr.sort()
                    except:
                        pass
                    try:
                        group_attr.sort()
                    except:
                        pass
                if (group_attr != module_attr):
                    changed = True
                    setattr(as_group, attr, module_attr)
        if (len(set_tags) > 0):
            have_tags = {
                
            }
            want_tags = {
                
            }
            for tag in asg_tags:
                want_tags[tag.key] = [tag.value, tag.propagate_at_launch]
            dead_tags = []
            if getattr(as_group, 'tags', None):
                for tag in as_group.tags:
                    have_tags[tag.key] = [tag.value, tag.propagate_at_launch]
                    if (tag.key not in want_tags):
                        changed = True
                        dead_tags.append(tag)
            elif ((getattr(as_group, 'tags', None) is None) and asg_tags):
                module.warn('It appears your ASG is attached to a target group. This is a boto2 bug. Tags will be added but no tags are able to be removed.')
            if (dead_tags != []):
                connection.delete_tags(dead_tags)
            if (have_tags != want_tags):
                changed = True
                connection.create_or_update_tags(asg_tags)
        load_balancers = (module.params.get('load_balancers') or [])
        if (load_balancers and (as_group.load_balancers != load_balancers)):
            changed = True
            as_group.load_balancers = module.params.get('load_balancers')
        if changed:
            try:
                as_group.update()
            except BotoServerError as e:
                module.fail_json(msg=('Failed to update Autoscaling Group: %s' % str(e)), exception=traceback.format_exc())
        if notification_topic:
            try:
                as_group.put_notification_configuration(notification_topic, notification_types)
            except BotoServerError as e:
                module.fail_json(msg=('Failed to update Autoscaling Group notifications: %s' % str(e)), exception=traceback.format_exc())
        if wait_for_instances:
            wait_for_new_inst(module, connection, group_name, wait_timeout, desired_capacity, 'viable_instances')
            wait_for_elb(connection, module, group_name)
        try:
            as_group = connection.get_all_groups(names=[group_name])[0]
            asg_properties = get_properties(as_group)
        except BotoServerError as e:
            module.fail_json(msg=('Failed to read existing Autoscaling Groups: %s' % str(e)), exception=traceback.format_exc())
        return (changed, asg_properties)
