def main():
    argument_spec = openstack_full_argument_spec(coe=dict(required=True, choices=['kubernetes', 'swarm', 'mesos']), dns_nameserver=dict(default='8.8.8.8'), docker_storage_driver=dict(choices=['devicemapper', 'overlay', 'overlay2']), docker_volume_size=dict(type='int'), external_network_id=dict(default=None), fixed_network=dict(default=None), fixed_subnet=dict(default=None), flavor_id=dict(default=None), floating_ip_enabled=dict(type='bool', default=True), keypair_id=dict(default=None), image_id=dict(required=True), labels=dict(default=None, type='raw'), http_proxy=dict(default=None), https_proxy=dict(default=None), master_lb_enabled=dict(type='bool', default=False), master_flavor_id=dict(default=None), name=dict(required=True), network_driver=dict(choices=['flannel', 'calico', 'docker']), no_proxy=dict(default=None), public=dict(type='bool', default=False), registry_enabled=dict(type='bool', default=False), server_type=dict(default='vm', choices=['vm', 'bm']), state=dict(default='present', choices=['absent', 'present']), tls_disabled=dict(type='bool', default=False), volume_driver=dict(choices=['cinder', 'rexray']))
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, **module_kwargs)
    params = module.params.copy()
    state = module.params['state']
    name = module.params['name']
    coe = module.params['coe']
    image_id = module.params['image_id']
    kwargs = dict(dns_nameserver=module.params['dns_nameserver'], docker_storage_driver=module.params['docker_storage_driver'], docker_volume_size=module.params['docker_volume_size'], external_network_id=module.params['external_network_id'], fixed_network=module.params['fixed_network'], fixed_subnet=module.params['fixed_subnet'], flavor_id=module.params['flavor_id'], floating_ip_enabled=module.params['floating_ip_enabled'], keypair_id=module.params['keypair_id'], labels=_parse_labels(params['labels']), http_proxy=module.params['http_proxy'], https_proxy=module.params['https_proxy'], master_lb_enabled=module.params['master_lb_enabled'], master_flavor_id=module.params['master_flavor_id'], network_driver=module.params['network_driver'], no_proxy=module.params['no_proxy'], public=module.params['public'], registry_enabled=module.params['registry_enabled'], server_type=module.params['server_type'], tls_disabled=module.params['tls_disabled'], volume_driver=module.params['volume_driver'])
    (sdk, cloud) = openstack_cloud_from_module(module)
    try:
        changed = False
        template = cloud.get_coe_cluster_template(name_or_id=name, filters={
            'coe': coe,
            'image_id': image_id,
        })
        if (state == 'present'):
            if (not template):
                template = cloud.create_coe_cluster_template(name, coe=coe, image_id=image_id, **kwargs)
                changed = True
            else:
                changed = False
            module.exit_json(changed=changed, cluster_template=template, id=template['uuid'])
        elif (state == 'absent'):
            if (not template):
                module.exit_json(changed=False)
            else:
                cloud.delete_coe_cluster_template(name)
                module.exit_json(changed=True)
    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e), extra_data=e.extra_data)