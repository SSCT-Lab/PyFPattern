def get_instances_by_lc(props, lc_check, initial_instances):
    new_instances = []
    old_instances = []
    if lc_check:
        for i in props['instances']:
            if (props['instance_facts'][i]['launch_config_name'] == props['launch_config_name']):
                new_instances.append(i)
            else:
                old_instances.append(i)
    else:
        log.debug('Comparing initial instances with current: %s', initial_instances)
        for i in props['instances']:
            if (i not in initial_instances):
                new_instances.append(i)
            else:
                old_instances.append(i)
    log.debug('New instances: %s, %s', len(new_instances), new_instances)
    log.debug('Old instances: %s, %s', len(old_instances), old_instances)
    return (new_instances, old_instances)