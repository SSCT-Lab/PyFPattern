def main():
    argument_spec = openstack_full_argument_spec(name=dict(required=True), shared=dict(default=False, type='bool'), admin_state_up=dict(default=True, type='bool'), external=dict(default=False, type='bool'), provider_physical_network=dict(required=False), provider_network_type=dict(required=False), provider_segmentation_id=dict(required=False, type='int'), state=dict(default='present', choices=['absent', 'present']), project=dict(default=None), port_security_enabled=dict(default=False, type='bool'))
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, **module_kwargs)
    state = module.params['state']
    name = module.params['name']
    shared = module.params['shared']
    admin_state_up = module.params['admin_state_up']
    external = module.params['external']
    provider_physical_network = module.params['provider_physical_network']
    provider_network_type = module.params['provider_network_type']
    provider_segmentation_id = module.params['provider_segmentation_id']
    project = module.params.get('project')
    port_security_enabled = module.params['port_security_enabled']
    (sdk, cloud) = openstack_cloud_from_module(module)
    try:
        if (project is not None):
            proj = cloud.get_project(project)
            if (proj is None):
                module.fail_json(msg=('Project %s could not be found' % project))
            project_id = proj['id']
            filters = {
                'tenant_id': project_id,
            }
        else:
            project_id = None
            filters = None
        net = cloud.get_network(name, filters=filters)
        if (state == 'present'):
            if (not net):
                provider = {
                    
                }
                if provider_physical_network:
                    provider['physical_network'] = provider_physical_network
                if provider_network_type:
                    provider['network_type'] = provider_network_type
                if provider_segmentation_id:
                    provider['segmentation_id'] = provider_segmentation_id
                if (project_id is not None):
                    net = cloud.create_network(name, shared, admin_state_up, external, provider, project_id, port_security_enabled=port_security_enabled)
                else:
                    net = cloud.create_network(name, shared, admin_state_up, external, provider, port_security_enabled=port_security_enabled)
                changed = True
            else:
                changed = False
            module.exit_json(changed=changed, network=net, id=net['id'])
        elif (state == 'absent'):
            if (not net):
                module.exit_json(changed=False)
            else:
                cloud.delete_network(name)
                module.exit_json(changed=True)
    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e))