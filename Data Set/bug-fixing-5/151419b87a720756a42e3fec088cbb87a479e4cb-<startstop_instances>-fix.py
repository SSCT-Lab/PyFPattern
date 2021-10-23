def startstop_instances(module, ec2, instance_ids, state, instance_tags):
    '\n    Starts or stops a list of existing instances\n\n    module: Ansible module object\n    ec2: authenticated ec2 connection object\n    instance_ids: The list of instances to start in the form of\n      [ {id: <inst-id>}, ..]\n    instance_tags: A dict of tag keys and values in the form of\n      {key: value, ... }\n    state: Intended state ("running" or "stopped")\n\n    Returns a dictionary of instance information\n    about the instances started/stopped.\n\n    If the instance was not able to change state,\n    "changed" will be set to False.\n\n    Note that if instance_ids and instance_tags are both non-empty,\n    this method will process the intersection of the two\n    '
    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))
    group_id = module.params.get('group_id')
    group_name = module.params.get('group')
    changed = False
    instance_dict_array = []
    if ((not isinstance(instance_ids, list)) or (len(instance_ids) < 1)):
        if (not instance_tags):
            module.fail_json(msg='instance_ids should be a list of instances, aborting')
    filters = {
        
    }
    if instance_tags:
        for (key, value) in instance_tags.items():
            filters[('tag:' + key)] = value
    if module.params.get('id'):
        filters['client-token'] = module.params['id']
    existing_instances_array = []
    for res in ec2.get_all_instances(instance_ids, filters=filters):
        for inst in res.instances:
            warn_if_public_ip_assignment_changed(module, inst)
            changed = (check_source_dest_attr(module, inst, ec2) or check_termination_protection(module, inst) or changed)
            if (inst.vpc_id and group_name):
                grp_details = ec2.get_all_security_groups(filters={
                    'vpc_id': inst.vpc_id,
                })
                if isinstance(group_name, string_types):
                    group_name = [group_name]
                unmatched = (set(group_name) - set((to_text(grp.name) for grp in grp_details)))
                if unmatched:
                    module.fail_json(msg=('The following group names are not valid: %s' % ', '.join(unmatched)))
                group_ids = [to_text(grp.id) for grp in grp_details if (to_text(grp.name) in group_name)]
            elif (inst.vpc_id and group_id):
                if isinstance(group_id, string_types):
                    group_id = [group_id]
                grp_details = ec2.get_all_security_groups(group_ids=group_id)
                group_ids = [grp_item.id for grp_item in grp_details]
            if (inst.vpc_id and (group_name or group_id)):
                if (set((sg.id for sg in inst.groups)) != set(group_ids)):
                    changed = inst.modify_attribute('groupSet', group_ids)
            if (inst.state != state):
                instance_dict_array.append(get_instance_info(inst))
                try:
                    if (state == 'running'):
                        inst.start()
                    else:
                        inst.stop()
                except EC2ResponseError as e:
                    module.fail_json(msg='Unable to change state for instance {0}, error: {1}'.format(inst.id, e))
                changed = True
            existing_instances_array.append(inst.id)
    instance_ids = list(set((existing_instances_array + (instance_ids or []))))
    wait_timeout = (time.time() + wait_timeout)
    while (wait and (wait_timeout > time.time())):
        instance_dict_array = []
        matched_instances = []
        for res in ec2.get_all_instances(instance_ids):
            for i in res.instances:
                if (i.state == state):
                    instance_dict_array.append(get_instance_info(i))
                    matched_instances.append(i)
        if (len(matched_instances) < len(instance_ids)):
            time.sleep(5)
        else:
            break
    if (wait and (wait_timeout <= time.time())):
        module.fail_json(msg=('wait for instances running timeout on %s' % time.asctime()))
    return (changed, instance_dict_array, instance_ids)