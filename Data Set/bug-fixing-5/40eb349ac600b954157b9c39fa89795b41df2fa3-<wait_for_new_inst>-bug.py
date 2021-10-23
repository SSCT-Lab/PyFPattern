def wait_for_new_inst(module, connection, group_name, wait_timeout, desired_size, prop):
    as_group = connection.describe_auto_scaling_groups(AutoScalingGroupNames=[group_name])['AutoScalingGroups'][0]
    props = get_properties(as_group, module)
    log.debug('Waiting for {0} = {1}, currently {2}'.format(prop, desired_size, props[prop]))
    wait_timeout = (time.time() + wait_timeout)
    while ((wait_timeout > time.time()) and (desired_size > props[prop])):
        log.debug('Waiting for {0} = {1}, currently {2}'.format(prop, desired_size, props[prop]))
        time.sleep(10)
        as_group = connection.describe_auto_scaling_groups(AutoScalingGroupNames=[group_name])['AutoScalingGroups'][0]
        props = get_properties(as_group, module)
    if (wait_timeout <= time.time()):
        module.fail_json(msg=('Waited too long for new instances to become viable. %s' % time.asctime()))
    log.debug('Reached {0}: {1}'.format(prop, desired_size))
    return props