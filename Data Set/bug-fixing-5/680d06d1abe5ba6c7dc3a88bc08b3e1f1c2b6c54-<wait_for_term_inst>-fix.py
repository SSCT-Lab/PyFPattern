def wait_for_term_inst(connection, term_instances):
    wait_timeout = module.params.get('wait_timeout')
    group_name = module.params.get('name')
    as_group = describe_autoscaling_groups(connection, group_name)[0]
    props = get_properties(as_group)
    count = 1
    wait_timeout = (time.time() + wait_timeout)
    while ((wait_timeout > time.time()) and (count > 0)):
        module.debug('waiting for instances to terminate')
        count = 0
        as_group = describe_autoscaling_groups(connection, group_name)[0]
        props = get_properties(as_group)
        instance_facts = props['instance_facts']
        instances = (i for i in instance_facts if (i in term_instances))
        for i in instances:
            lifecycle = instance_facts[i]['lifecycle_state']
            health = instance_facts[i]['health_status']
            module.debug(('Instance %s has state of %s,%s' % (i, lifecycle, health)))
            if ((lifecycle == 'Terminating') or (health == 'Unhealthy')):
                count += 1
        time.sleep(10)
    if (wait_timeout <= time.time()):
        module.fail_json(msg=('Waited too long for old instances to terminate. %s' % time.asctime()))