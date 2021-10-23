

def find_running_instances_by_count_tag(module, ec2, vpc, count_tag, zone=None):
    state = module.params.get('state')
    if (state not in ['running', 'stopped']):
        state = None
    reservations = get_reservations(module, ec2, vpc, tags=count_tag, state=state, zone=zone)
    instances = []
    for res in reservations:
        if hasattr(res, 'instances'):
            for inst in res.instances:
                if (inst.state == 'terminated'):
                    continue
                instances.append(inst)
    return (reservations, instances)
