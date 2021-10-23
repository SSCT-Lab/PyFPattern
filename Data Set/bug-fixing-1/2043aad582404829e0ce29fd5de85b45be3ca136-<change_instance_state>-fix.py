

@AWSRetry.jittered_backoff()
def change_instance_state(filters, desired_state, ec2=None):
    'Takes STOPPED/RUNNING/TERMINATED'
    if (ec2 is None):
        ec2 = module.client('ec2')
    changed = set()
    instances = find_instances(ec2, filters=filters)
    to_change = set((i['InstanceId'] for i in instances if (i['State']['Name'].upper() != desired_state)))
    unchanged = set()
    for inst in instances:
        try:
            if (desired_state == 'TERMINATED'):
                if module.check_mode:
                    changed.add(inst['InstanceId'])
                    continue
                resp = ec2.terminate_instances(InstanceIds=[inst['InstanceId']])
                [changed.add(i['InstanceId']) for i in resp['TerminatingInstances']]
            if (desired_state == 'STOPPED'):
                if (inst['State']['Name'] in ('stopping', 'stopped')):
                    unchanged.add(inst['InstanceId'])
                    continue
                if module.check_mode:
                    changed.add(inst['InstanceId'])
                    continue
                resp = ec2.stop_instances(InstanceIds=[inst['InstanceId']])
                [changed.add(i['InstanceId']) for i in resp['StoppingInstances']]
            if (desired_state == 'RUNNING'):
                if module.check_mode:
                    changed.add(inst['InstanceId'])
                    continue
                resp = ec2.start_instances(InstanceIds=[inst['InstanceId']])
                [changed.add(i['InstanceId']) for i in resp['StartingInstances']]
        except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError):
            pass
    if changed:
        await_instances(ids=(list(changed) + list(unchanged)), state=desired_state)
    change_failed = list((to_change - changed))
    instances = find_instances(ec2, ids=list((i['InstanceId'] for i in instances)))
    return (changed, change_failed, instances)
