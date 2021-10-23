

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state=dict(required=True, choices=['present', 'absent', 'deleting']), name=dict(required=True, type='str'), cluster=dict(required=False, type='str'), task_definition=dict(required=False, type='str'), load_balancers=dict(required=False, default=[], type='list'), desired_count=dict(required=False, type='int'), client_token=dict(required=False, default='', type='str'), role=dict(required=False, default='', type='str'), delay=dict(required=False, type='int', default=10), repeat=dict(required=False, type='int', default=10)))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[('state', 'present', ['task_definition', 'desired_count'])], required_together=[['load_balancers', 'role']])
    if (not HAS_BOTO):
        module.fail_json(msg='boto is required.')
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 is required.')
    service_mgr = EcsServiceManager(module)
    try:
        existing = service_mgr.describe_service(module.params['cluster'], module.params['name'])
    except Exception as e:
        module.fail_json(msg=((((("Exception describing service '" + module.params['name']) + "' in cluster '") + module.params['cluster']) + "': ") + str(e)))
    results = dict(changed=False)
    if (module.params['state'] == 'present'):
        matching = False
        update = False
        if (existing and ('status' in existing) and (existing['status'] == 'ACTIVE')):
            if service_mgr.is_matching_service(module.params, existing):
                matching = True
                results['service'] = service_mgr.jsonize(existing)
            else:
                update = True
        if (not matching):
            if (not module.check_mode):
                loadBalancers = module.params['load_balancers']
                role = module.params['role']
                clientToken = module.params['client_token']
                if update:
                    response = service_mgr.update_service(module.params['name'], module.params['cluster'], module.params['task_definition'], loadBalancers, module.params['desired_count'], clientToken, role)
                else:
                    response = service_mgr.create_service(module.params['name'], module.params['cluster'], module.params['task_definition'], loadBalancers, module.params['desired_count'], clientToken, role)
                results['service'] = response
            results['changed'] = True
    elif (module.params['state'] == 'absent'):
        if (not existing):
            pass
        else:
            del existing['deployments']
            del existing['events']
            results['ansible_facts'] = existing
            if (('status' in existing) and (existing['status'] == 'INACTIVE')):
                results['changed'] = False
            else:
                if (not module.check_mode):
                    try:
                        service_mgr.delete_service(module.params['name'], module.params['cluster'])
                    except botocore.exceptions.ClientError as e:
                        module.fail_json(msg=e.message)
                results['changed'] = True
    elif (module.params['state'] == 'deleting'):
        if (not existing):
            module.fail_json(msg=(("Service '" + module.params['name']) + ' not found.'))
            return
        delay = module.params['delay']
        repeat = module.params['repeat']
        time.sleep(delay)
        for i in range(repeat):
            existing = service_mgr.describe_service(module.params['cluster'], module.params['name'])
            status = existing['status']
            if (status == 'INACTIVE'):
                results['changed'] = True
                break
            time.sleep(delay)
        if (i is (repeat - 1)):
            module.fail_json(msg=(((('Service still not deleted after ' + str(repeat)) + ' tries of ') + str(delay)) + ' seconds each.'))
            return
    module.exit_json(**results)
