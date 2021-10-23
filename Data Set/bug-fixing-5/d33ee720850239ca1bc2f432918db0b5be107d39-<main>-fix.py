def main():
    argument_spec = openstack_full_argument_spec(uuid=dict(required=False), name=dict(required=False), instance_info=dict(type='dict', required=False), config_drive=dict(required=False), ironic_url=dict(required=False), state=dict(required=False, default='present'), maintenance=dict(required=False), maintenance_reason=dict(required=False), power=dict(required=False, default='present'), deploy=dict(required=False, default=True), wait=dict(type='bool', required=False, default=False), timeout=dict(required=False, type='int', default=1800))
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, **module_kwargs)
    if ((module.params['auth_type'] in [None, 'None']) and (module.params['ironic_url'] is None)):
        module.fail_json(msg='Authentication appears disabled, Please define an ironic_url parameter')
    if (module.params['ironic_url'] and (module.params['auth_type'] in [None, 'None'])):
        module.params['auth'] = dict(endpoint=module.params['ironic_url'])
    node_id = _choose_id_value(module)
    if (not node_id):
        module.fail_json(msg='A uuid or name value must be defined to use this module.')
    (sdk, cloud) = openstack_cloud_from_module(module)
    try:
        node = cloud.get_machine(node_id)
        if (node is None):
            module.fail_json(msg='node not found')
        uuid = node['uuid']
        instance_info = module.params['instance_info']
        changed = False
        wait = module.params['wait']
        timeout = module.params['timeout']
        if (module.params['state'] == 'maintenance'):
            module.params['maintenance'] = True
        if (node['provision_state'] in ['cleaning', 'deleting', 'wait call-back']):
            module.fail_json(msg=('Node is in %s state, cannot act upon the request as the node is in a transition state' % node['provision_state']))
        if _check_set_maintenance(module, cloud, node):
            if (node['provision_state'] in 'active'):
                module.exit_json(changed=True, result='Maintenance state changed')
            changed = True
            node = cloud.get_machine(node_id)
        if _check_set_power_state(module, cloud, node):
            changed = True
            node = cloud.get_machine(node_id)
        if _is_true(module.params['state']):
            if _is_false(module.params['deploy']):
                module.exit_json(changed=changed, result='User request has explicitly disabled deployment logic')
            if ('active' in node['provision_state']):
                module.exit_json(changed=changed, result='Node already in an active state.')
            if (instance_info is None):
                module.fail_json(changed=changed, msg='When setting an instance to present, instance_info is a required variable.')
            cloud.update_machine(uuid, instance_info=instance_info)
            cloud.validate_node(uuid)
            if (not wait):
                cloud.activate_node(uuid, module.params['config_drive'])
            else:
                cloud.activate_node(uuid, configdrive=module.params['config_drive'], wait=wait, timeout=timeout)
            module.exit_json(changed=changed, result='node activated')
        elif _is_false(module.params['state']):
            if (node['provision_state'] not in 'deleted'):
                cloud.update_machine(uuid, instance_info={
                    
                })
                if (not wait):
                    cloud.deactivate_node(uuid)
                else:
                    cloud.deactivate_node(uuid, wait=wait, timeout=timeout)
                module.exit_json(changed=True, result='deleted')
            else:
                module.exit_json(changed=False, result='node not found')
        else:
            module.fail_json(msg='State must be present, absent, maintenance, off')
    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e))