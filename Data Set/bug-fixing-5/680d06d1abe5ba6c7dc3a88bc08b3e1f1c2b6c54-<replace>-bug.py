def replace(connection, module):
    batch_size = module.params.get('replace_batch_size')
    wait_timeout = module.params.get('wait_timeout')
    group_name = module.params.get('name')
    max_size = module.params.get('max_size')
    min_size = module.params.get('min_size')
    desired_capacity = module.params.get('desired_capacity')
    lc_check = module.params.get('lc_check')
    replace_instances = module.params.get('replace_instances')
    as_group = describe_autoscaling_groups(connection, group_name)[0]
    wait_for_new_inst(module, connection, group_name, wait_timeout, as_group['MinSize'], 'viable_instances')
    props = get_properties(as_group, module)
    instances = props['instances']
    if replace_instances:
        instances = replace_instances
    (new_instances, old_instances) = get_instances_by_lc(props, lc_check, instances)
    num_new_inst_needed = (desired_capacity - len(new_instances))
    if lc_check:
        if ((num_new_inst_needed == 0) and old_instances):
            log.debug('No new instances needed, but old instances are present. Removing old instances')
            terminate_batch(connection, module, old_instances, instances, True)
            as_group = describe_autoscaling_groups(connection, group_name)[0]
            props = get_properties(as_group, module)
            changed = True
            return (changed, props)
        if (num_new_inst_needed < batch_size):
            log.debug('Overriding batch size to %s', num_new_inst_needed)
            batch_size = num_new_inst_needed
    if (not old_instances):
        changed = False
        return (changed, props)
    if (min_size is None):
        min_size = as_group['MinSize']
    if (max_size is None):
        max_size = as_group['MaxSize']
    if (desired_capacity is None):
        desired_capacity = as_group['DesiredCapacity']
    as_group = describe_autoscaling_groups(connection, group_name)[0]
    update_size(connection, as_group, (max_size + batch_size), (min_size + batch_size), (desired_capacity + batch_size))
    wait_for_new_inst(module, connection, group_name, wait_timeout, as_group['MinSize'], 'viable_instances')
    wait_for_elb(connection, module, group_name)
    wait_for_target_group(connection, module, group_name)
    as_group = describe_autoscaling_groups(connection, group_name)[0]
    props = get_properties(as_group, module)
    instances = props['instances']
    if replace_instances:
        instances = replace_instances
    log.debug('beginning main loop')
    for i in get_chunks(instances, batch_size):
        (break_early, desired_size, term_instances) = terminate_batch(connection, module, i, instances, False)
        wait_for_term_inst(connection, module, term_instances)
        wait_for_new_inst(module, connection, group_name, wait_timeout, desired_size, 'viable_instances')
        wait_for_elb(connection, module, group_name)
        wait_for_target_group(connection, module, group_name)
        as_group = describe_autoscaling_groups(connection, group_name)[0]
        if break_early:
            log.debug('breaking loop')
            break
    update_size(connection, as_group, max_size, min_size, desired_capacity)
    as_group = describe_autoscaling_groups(connection, group_name)[0]
    asg_properties = get_properties(as_group, module)
    log.debug('Rolling update complete.')
    changed = True
    return (changed, asg_properties)