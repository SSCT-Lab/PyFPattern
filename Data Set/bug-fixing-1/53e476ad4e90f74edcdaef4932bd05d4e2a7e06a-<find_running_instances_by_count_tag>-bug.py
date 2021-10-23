

def find_running_instances_by_count_tag(module, ec2, vpc, count_tag, zone=None):
    reservations = get_reservations(module, ec2, vpc, tags=count_tag, state='running', zone=zone)
    instances = []
    for res in reservations:
        if hasattr(res, 'instances'):
            for inst in res.instances:
                instances.append(inst)
    return (reservations, instances)
