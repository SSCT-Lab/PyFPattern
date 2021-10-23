def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state=dict(required=True, choices=['present', 'absent', 'deleting']), name=dict(required=True, type='str'), cluster=dict(required=False, type='str'), task_definition=dict(required=False, type='str'), load_balancers=dict(required=False, default=[], type='list'), desired_count=dict(required=False, type='int'), client_token=dict(required=False, default='', type='str'), role=dict(required=False, default='', type='str'), delay=dict(required=False, type='int', default=10), repeat=dict(required=False, type='int', default=10), deployment_configuration=dict(required=False, default={
        
    }, type='dict'), placement_constraints=dict(required=False, default=[], type='list'), placement_strategy=dict(required=False, default=[], type='list'), network_configuration=dict(required=False, type='dict', options=dict(subnets=dict(type='list'), security_groups=dict(type='list'), assign_public_ip=dict(type='bool'))), launch_type=dict(required=False, choices=['EC2', 'FARGATE'])))
    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[('state', 'present', ['task_definition', 'desired_count']), ('launch_type', 'FARGATE', ['network_configuration'])], required_together=[['load_balancers', 'role']])
    service_mgr = EcsServiceManager(module)
    if module.params['network_configuration']:
        if (not service_mgr.ecs_api_handles_network_configuration()):
            module.fail_json(msg='botocore needs to be version 1.7.44 or higher to use network configuration')
        network_configuration = service_mgr.format_network_configuration(module.params['network_configuration'])
    else:
        network_configuration = None
    deployment_configuration = map_complex_type(module.params['deployment_configuration'], DEPLOYMENT_CONFIGURATION_TYPE_MAP)
    deploymentConfiguration = snake_dict_to_camel_dict(deployment_configuration)
    try:
        existing = service_mgr.describe_service(module.params['cluster'], module.params['name'])
    except Exception as e:
        module.fail_json(msg=((((("Exception describing service '" + module.params['name']) + "' in cluster '") + module.params['cluster']) + "': ") + str(e)))
    results = dict(changed=False)
    if module.params['launch_type']:
        if (not module.botocore_at_least('1.8.4')):
            module.fail_json(msg='botocore needs to be version 1.8.4 or higher to use launch_type')
    if (module.params['state'] == 'present'):
        matching = False
        update = False
        if (existing and ('status' in existing) and (existing['status'] == 'ACTIVE')):
            if service_mgr.is_matching_service(module.params, existing):
                matching = True
                results['service'] = existing
            else:
                update = True
        if (not matching):
            if (not module.check_mode):
                role = module.params['role']
                clientToken = module.params['client_token']
                loadBalancers = []
                for loadBalancer in module.params['load_balancers']:
                    if ('containerPort' in loadBalancer):
                        loadBalancer['containerPort'] = int(loadBalancer['containerPort'])
                    loadBalancers.append(loadBalancer)
                if update:
                    if ((existing['loadBalancers'] or []) != loadBalancers):
                        module.fail_json(msg='It is not possible to update the load balancers of an existing service')
                    response = service_mgr.update_service(module.params['name'], module.params['cluster'], module.params['task_definition'], module.params['desired_count'], deploymentConfiguration, network_configuration)
                else:
                    try:
                        response = service_mgr.create_service(module.params['name'], module.params['cluster'], module.params['task_definition'], loadBalancers, module.params['desired_count'], clientToken, role, deploymentConfiguration, module.params['placement_constraints'], module.params['placement_strategy'], network_configuration, module.params['launch_type'])
                    except botocore.exceptions.ClientError as e:
                        module.fail_json_aws(e, msg="Couldn't create service")
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
                        module.fail_json_aws(e, msg="Couldn't delete service")
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