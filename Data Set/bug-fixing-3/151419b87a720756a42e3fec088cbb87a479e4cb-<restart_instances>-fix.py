def restart_instances(module, ec2, instance_ids, state, instance_tags):
    '\n    Restarts a list of existing instances\n\n    module: Ansible module object\n    ec2: authenticated ec2 connection object\n    instance_ids: The list of instances to start in the form of\n      [ {id: <inst-id>}, ..]\n    instance_tags: A dict of tag keys and values in the form of\n      {key: value, ... }\n    state: Intended state ("restarted")\n\n    Returns a dictionary of instance information\n    about the instances.\n\n    If the instance was not able to change state,\n    "changed" will be set to False.\n\n    Wait will not apply here as this is a OS level operation.\n\n    Note that if instance_ids and instance_tags are both non-empty,\n    this method will process the intersection of the two.\n    '
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
    for res in ec2.get_all_instances(instance_ids, filters=filters):
        for inst in res.instances:
            warn_if_public_ip_assignment_changed(module, inst)
            changed = (check_source_dest_attr(module, inst, ec2) or check_termination_protection(module, inst) or changed)
            if (inst.state != state):
                instance_dict_array.append(get_instance_info(inst))
                try:
                    inst.reboot()
                except EC2ResponseError as e:
                    module.fail_json(msg='Unable to change state for instance {0}, error: {1}'.format(inst.id, e))
                changed = True
    return (changed, instance_dict_array, instance_ids)