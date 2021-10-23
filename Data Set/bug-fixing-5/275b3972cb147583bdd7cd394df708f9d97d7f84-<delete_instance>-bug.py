def delete_instance(module, client, instance_name):
    '\n    Terminates an instance\n\n    module: Ansible module object\n    client: authenticated lightsail connection object\n    instance_name: name of instance to delete\n\n    Returns a dictionary of instance information\n    about the instance deleted (pre-deletion).\n\n    If the instance to be deleted is running\n    "changed" will be set to False.\n\n    '
    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))
    wait_max = (time.time() + wait_timeout)
    changed = False
    inst = None
    try:
        inst = _find_instance_info(client, instance_name)
    except botocore.exceptions.ClientError as e:
        if (e.response['Error']['Code'] != 'NotFoundException'):
            module.fail_json(msg='Error finding instance {0}, error: {1}'.format(instance_name, e))
    if wait:
        while ((wait_max > time.time()) and (inst is not None) and (inst['state']['name'] in ('pending', 'stopping'))):
            try:
                time.sleep(5)
                inst = _find_instance_info(client, instance_name)
            except botocore.exceptions.ClientError as e:
                if (e.response['ResponseMetadata']['HTTPStatusCode'] == '403'):
                    module.fail_json(msg='Failed to delete instance {0}. Check that you have permissions to perform the operation.'.format(instance_name), exception=traceback.format_exc())
                elif (e.response['Error']['Code'] == 'RequestExpired'):
                    module.fail_json(msg='RequestExpired: Failed to delete instance {0}.'.format(instance_name), exception=traceback.format_exc())
                time.sleep(10)
    if (inst is not None):
        while ((not changed) and ((wait and (wait_max > time.time())) or (not wait))):
            try:
                client.delete_instance(instanceName=instance_name)
                changed = True
            except botocore.exceptions.ClientError as e:
                module.fail_json(msg='Error deleting instance {0}, error: {1}'.format(instance_name, e))
    if (wait and (not changed) and (wait_max <= time.time())):
        module.fail_json(msg=('wait for instance delete timeout at %s' % time.asctime()))
    return (changed, inst)