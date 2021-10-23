def find_running_instances_by_count_tag(module, ec2, count_tag, zone=None):
    reservations = get_reservations(module, ec2, tags=count_tag, state='running', zone=zone)
    instances = []
    for res in reservations:
        if hasattr(res, 'instances'):
            for inst in res.instances:
                instances.append(inst)
    return (reservations, instances)