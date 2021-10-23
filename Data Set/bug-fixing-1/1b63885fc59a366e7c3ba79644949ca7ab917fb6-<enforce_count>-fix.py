

def enforce_count(module, ec2, vpc):
    exact_count = module.params.get('exact_count')
    count_tag = module.params.get('count_tag')
    zone = module.params.get('zone')
    if (exact_count and (count_tag is None)):
        module.fail_json(msg="you must use the 'count_tag' option with exact_count")
    (reservations, instances) = find_running_instances_by_count_tag(module, ec2, vpc, count_tag, zone)
    changed = None
    checkmode = False
    instance_dict_array = []
    changed_instance_ids = None
    if (len(instances) == exact_count):
        changed = False
    elif (len(instances) < exact_count):
        changed = True
        to_create = (exact_count - len(instances))
        if (not checkmode):
            (instance_dict_array, changed_instance_ids, changed) = create_instances(module, ec2, vpc, override_count=to_create)
            for inst in instance_dict_array:
                instances.append(inst)
    elif (len(instances) > exact_count):
        changed = True
        to_remove = (len(instances) - exact_count)
        if (not checkmode):
            all_instance_ids = sorted([x.id for x in instances])
            remove_ids = all_instance_ids[0:to_remove]
            instances = [x for x in instances if (x.id not in remove_ids)]
            (changed, instance_dict_array, changed_instance_ids) = terminate_instances(module, ec2, remove_ids)
            terminated_list = []
            for inst in instance_dict_array:
                inst['state'] = 'terminated'
                terminated_list.append(inst)
            instance_dict_array = terminated_list
    all_instances = []
    for inst in instances:
        warn_if_public_ip_assignment_changed(module, inst)
        if (not isinstance(inst, dict)):
            inst = get_instance_info(inst)
        all_instances.append(inst)
    return (all_instances, instance_dict_array, changed_instance_ids, changed)
