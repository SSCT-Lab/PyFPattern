def create_instance_template(module, gce):
    'Create an instance template\n    module : AnsibleModule object\n    gce: authenticated GCE libcloud driver\n    Returns:\n        instance template information\n    '
    name = module.params.get('name')
    size = module.params.get('size')
    source = module.params.get('source')
    image = module.params.get('image')
    image_family = module.params.get('image_family')
    disk_type = module.params.get('disk_type')
    disk_auto_delete = module.params.get('disk_auto_delete')
    network = module.params.get('network')
    subnetwork = module.params.get('subnetwork')
    subnetwork_region = module.params.get('subnetwork_region')
    can_ip_forward = module.params.get('can_ip_forward')
    external_ip = module.params.get('external_ip')
    service_account_email = module.params.get('service_account_email')
    service_account_permissions = module.params.get('service_account_permissions')
    on_host_maintenance = module.params.get('on_host_maintenance')
    automatic_restart = module.params.get('automatic_restart')
    preemptible = module.params.get('preemptible')
    tags = module.params.get('tags')
    metadata = module.params.get('metadata')
    description = module.params.get('description')
    disks = module.params.get('disks')
    changed = False
    gce_args = dict(name='instance', size='f1-micro', source=None, image=None, disk_type='pd-standard', disk_auto_delete=True, network='default', subnetwork=None, can_ip_forward=None, external_ip='ephemeral', service_accounts=None, on_host_maintenance=None, automatic_restart=None, preemptible=None, tags=None, metadata=None, description=None, disks_gce_struct=None, nic_gce_struct=None)
    gce_args['name'] = name
    gce_args['size'] = size
    if (source is not None):
        gce_args['source'] = source
    if image:
        gce_args['image'] = image
    elif image_family:
        image = gce.ex_get_image_from_family(image_family)
        gce_args['image'] = image
    else:
        gce_args['image'] = 'debian-8'
    gce_args['disk_type'] = disk_type
    gce_args['disk_auto_delete'] = disk_auto_delete
    gce_network = gce.ex_get_network(network)
    gce_args['network'] = gce_network
    if (subnetwork is not None):
        gce_args['subnetwork'] = gce.ex_get_subnetwork(subnetwork, region=subnetwork_region)
    if (can_ip_forward is not None):
        gce_args['can_ip_forward'] = can_ip_forward
    if (external_ip == 'ephemeral'):
        instance_external_ip = external_ip
    elif (external_ip == 'none'):
        instance_external_ip = None
    else:
        try:
            instance_external_ip = gce.ex_get_address(external_ip)
        except GoogleBaseError as err:
            instance_external_ip = external_ip
    gce_args['external_ip'] = instance_external_ip
    ex_sa_perms = []
    bad_perms = []
    if service_account_permissions:
        for perm in service_account_permissions:
            if (perm not in gce.SA_SCOPES_MAP):
                bad_perms.append(perm)
        if (len(bad_perms) > 0):
            module.fail_json(msg=('bad permissions: %s' % str(bad_perms)))
        ex_sa_perms.append({
            'email': 'default',
        })
        ex_sa_perms[0]['scopes'] = service_account_permissions
    gce_args['service_accounts'] = ex_sa_perms
    if (on_host_maintenance is not None):
        gce_args['on_host_maintenance'] = on_host_maintenance
    if (automatic_restart is not None):
        gce_args['automatic_restart'] = automatic_restart
    if (preemptible is not None):
        gce_args['preemptible'] = preemptible
    if (tags is not None):
        gce_args['tags'] = tags
    if metadata:
        if isinstance(metadata, dict):
            md = metadata
        else:
            try:
                md = literal_eval(str(metadata))
                if (not isinstance(md, dict)):
                    raise ValueError('metadata must be a dict')
            except ValueError as e:
                module.fail_json(msg=('bad metadata: %s' % str(e)))
            except SyntaxError as e:
                module.fail_json(msg='bad metadata syntax')
        if (hasattr(libcloud, '__version__') and (libcloud.__version__ < '0.15')):
            items = []
            for (k, v) in md.items():
                items.append({
                    'key': k,
                    'value': v,
                })
            metadata = {
                'items': items,
            }
        else:
            metadata = md
    gce_args['metadata'] = metadata
    if (description is not None):
        gce_args['description'] = description
    instance = None
    try:
        instance = gce.ex_get_instancetemplate(name)
    except ResourceNotFoundError:
        try:
            instance = gce.ex_create_instancetemplate(**gce_args)
            changed = True
        except GoogleBaseError as err:
            module.fail_json(msg='Unexpected error attempting to create instance {}, error: {}'.format(instance, err.value))
    if instance:
        json_data = get_info(instance)
    else:
        module.fail_json(msg='no instance template!')
    return (changed, json_data, name)