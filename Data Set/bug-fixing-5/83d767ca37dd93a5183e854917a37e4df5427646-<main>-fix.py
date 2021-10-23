def main():
    argument_spec = openstack_full_argument_spec(name=dict(required=True), shared=dict(default=False, type='bool'), admin_state_up=dict(default=True, type='bool'), external=dict(default=False, type='bool'), provider_physical_network=dict(required=False), provider_network_type=dict(required=False), provider_segmentation_id=dict(required=False), state=dict(default='present', choices=['absent', 'present']), project=dict(default=None))
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, **module_kwargs)
    if (not HAS_SHADE):
        module.fail_json(msg='shade is required for this module')
    if (module.params['project'] and (StrictVersion(shade.__version__) < StrictVersion('1.6.0'))):
        module.fail_json(msg='To utilize project, the installed version ofthe shade library MUST be >=1.6.0')
    state = module.params['state']
    name = module.params['name']
    shared = module.params['shared']
    admin_state_up = module.params['admin_state_up']
    external = module.params['external']
    provider_physical_network = module.params['provider_physical_network']
    provider_network_type = module.params['provider_network_type']
    provider_segmentation_id = module.params['provider_segmentation_id']
    project = module.params.pop('project')
    try:
        cloud = shade.openstack_cloud(**module.params)
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
                if (provider and (StrictVersion(shade.__version__) < StrictVersion('1.5.0'))):
                    module.fail_json(msg='Shade >= 1.5.0 required to use provider options')
                if (project_id is not None):
                    net = cloud.create_network(name, shared, admin_state_up, external, provider, project_id)
                else:
                    net = cloud.create_network(name, shared, admin_state_up, external, provider)
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
    except shade.OpenStackCloudException as e:
        module.fail_json(msg=str(e))