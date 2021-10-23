def suspend_processes(ec2_connection, as_group, module):
    suspend_processes = set(module.params.get('suspend_processes'))
    try:
        suspended_processes = set([p['ProcessName'] for p in as_group['SuspendedProcesses']])
    except AttributeError:
        suspended_processes = set()
    if (suspend_processes == suspended_processes):
        return False
    resume_processes = list((suspended_processes - suspend_processes))
    if resume_processes:
        resume_asg_processes(ec2_connection, module.params.get('name'), resume_processes)
    if suspend_processes:
        suspend_asg_processes(ec2_connection, module.params.get('name'), list(suspend_processes))
    return True