def main():
    argument_spec = openstack_full_argument_spec(server=dict(required=False), detailed=dict(required=False, type='bool'), filters=dict(required=False, type='dict', default=None))
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, **module_kwargs)
    (sdk, cloud) = openstack_cloud_from_module(module)
    try:
        openstack_servers = cloud.list_servers(detailed=module.params['detailed'])
        openstack_servers = cloud.search_servers(detailed=module.params['detailed'], filters=module.params['filters'])
        if module.params['server']:
            pattern = module.params['server']
            openstack_servers = [server for server in openstack_servers if (fnmatch.fnmatch(server['name'], pattern) or fnmatch.fnmatch(server['id'], pattern))]
        module.exit_json(changed=False, ansible_facts=dict(openstack_servers=openstack_servers))
    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e))