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
        ec2_connection.resume_processes(AutoScalingGroupName=module.params.get('name'), ScalingProcesses=resume_processes)
    if suspend_processes:
        ec2_connection.suspend_processes(AutoScalingGroupName=module.params.get('name'), ScalingProcesses=list(suspend_processes))
    return True