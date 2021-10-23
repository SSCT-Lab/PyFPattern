

def _create_server(module, cloud):
    flavor = module.params['flavor']
    flavor_ram = module.params['flavor_ram']
    flavor_include = module.params['flavor_include']
    image_id = None
    if (not module.params['boot_volume']):
        image_id = cloud.get_image_id(module.params['image'], module.params['image_exclude'])
        if (not image_id):
            module.fail_json(msg=('Could not find image %s' % module.params['image']))
    if flavor:
        flavor_dict = cloud.get_flavor(flavor)
        if (not flavor_dict):
            module.fail_json(msg=('Could not find flavor %s' % flavor))
    else:
        flavor_dict = cloud.get_flavor_by_ram(flavor_ram, flavor_include)
        if (not flavor_dict):
            module.fail_json(msg='Could not find any matching flavor')
    nics = _network_args(module, cloud)
    if isinstance(module.params['meta'], str):
        metas = {
            
        }
        for kv_str in module.params['meta'].split(','):
            (k, v) = kv_str.split('=')
            metas[k] = v
        module.params['meta'] = metas
    bootkwargs = dict(name=module.params['name'], image=image_id, flavor=flavor_dict['id'], nics=nics, meta=module.params['meta'], security_groups=module.params['security_groups'], userdata=module.params['userdata'], config_drive=module.params['config_drive'])
    for optional_param in ('key_name', 'availability_zone', 'network', 'scheduler_hints', 'volume_size', 'volumes'):
        if module.params[optional_param]:
            bootkwargs[optional_param] = module.params[optional_param]
    server = cloud.create_server(ip_pool=module.params['floating_ip_pools'], ips=module.params['floating_ips'], auto_ip=module.params['auto_ip'], boot_volume=module.params['boot_volume'], boot_from_volume=module.params['boot_from_volume'], terminate_volume=module.params['terminate_volume'], reuse_ips=module.params['reuse_ips'], wait=module.params['wait'], timeout=module.params['timeout'], **bootkwargs)
    _exit_hostvars(module, cloud, server)
