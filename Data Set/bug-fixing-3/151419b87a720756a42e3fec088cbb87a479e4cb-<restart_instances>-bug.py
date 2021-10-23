def restart_instances(module, ec2, instance_ids, state, instance_tags):
    '\n    Restarts a list of existing instances\n\n    module: Ansible module object\n    ec2: authenticated ec2 connection object\n    instance_ids: The list of instances to start in the form of\n      [ {id: <inst-id>}, ..]\n    instance_tags: A dict of tag keys and values in the form of\n      {key: value, ... }\n    state: Intended state ("restarted")\n\n    Returns a dictionary of instance information\n    about the instances.\n\n    If the instance was not able to change state,\n    "changed" will be set to False.\n\n    Wait will not apply here as this is a OS level operation.\n\n    Note that if instance_ids and instance_tags are both non-empty,\n    this method will process the intersection of the two.\n    '
    source_dest_check = module.params.get('source_dest_check')
    termination_protection = module.params.get('termination_protection')
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
            try:
                if ((inst.vpc_id is not None) and (inst.get_attribute('sourceDestCheck')['sourceDestCheck'] != source_dest_check)):
                    inst.modify_attribute('sourceDestCheck', source_dest_check)
                    changed = True
            except boto.exception.EC2ResponseError as exc:
                if (exc.code == 'InvalidInstanceID'):
                    for interface in inst.interfaces:
                        if (interface.source_dest_check != source_dest_check):
                            ec2.modify_network_interface_attribute(interface.id, 'sourceDestCheck', source_dest_check)
                            changed = True
                else:
                    module.fail_json(msg='Failed to handle source_dest_check state for instance {0}, error: {1}'.format(inst.id, exc), exception=traceback.format_exc())
            if ((inst.get_attribute('disableApiTermination')['disableApiTermination'] != termination_protection) and (termination_protection is not None)):
                inst.modify_attribute('disableApiTermination', termination_protection)
                changed = True
            if (inst.state != state):
                instance_dict_array.append(get_instance_info(inst))
                try:
                    inst.reboot()
                except EC2ResponseError as e:
                    module.fail_json(msg='Unable to change state for instance {0}, error: {1}'.format(inst.id, e))
                changed = True
    return (changed, instance_dict_array, instance_ids)