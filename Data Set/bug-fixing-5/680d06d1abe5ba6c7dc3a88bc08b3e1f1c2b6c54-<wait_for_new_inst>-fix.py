def wait_for_new_inst(connection, group_name, wait_timeout, desired_size, prop):
    as_group = describe_autoscaling_groups(connection, group_name)[0]
    props = get_properties(as_group)
    module.debug(('Waiting for %s = %s, currently %s' % (prop, desired_size, props[prop])))
    wait_timeout = (time.time() + wait_timeout)
    while ((wait_timeout > time.time()) and (desired_size > props[prop])):
        module.debug(('Waiting for %s = %s, currently %s' % (prop, desired_size, props[prop])))
        time.sleep(10)
        as_group = describe_autoscaling_groups(connection, group_name)[0]
        props = get_properties(as_group)
    if (wait_timeout <= time.time()):
        module.fail_json(msg=('Waited too long for new instances to become viable. %s' % time.asctime()))
    module.debug(('Reached %s: %s' % (prop, desired_size)))
    return props