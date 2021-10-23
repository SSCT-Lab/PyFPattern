def create_instances(module, gce, instance_names, number, lc_zone):
    "Creates new instances. Attributes other than instance_names are picked\n    up from 'module'\n\n    module : AnsibleModule object\n    gce: authenticated GCE libcloud driver\n    instance_names: python list of instance names to create\n    number: number of instances to create\n    lc_zone: GCEZone object\n\n    Returns:\n        A list of dictionaries with instance information\n        about the instances that were launched.\n\n    "
    image = module.params.get('image')
    machine_type = module.params.get('machine_type')
    metadata = module.params.get('metadata')
    network = module.params.get('network')
    subnetwork = module.params.get('subnetwork')
    persistent_boot_disk = module.params.get('persistent_boot_disk')
    disks = module.params.get('disks')
    state = module.params.get('state')
    tags = module.params.get('tags')
    ip_forward = module.params.get('ip_forward')
    external_ip = module.params.get('external_ip')
    disk_auto_delete = module.params.get('disk_auto_delete')
    preemptible = module.params.get('preemptible')
    disk_size = module.params.get('disk_size')
    service_account_permissions = module.params.get('service_account_permissions')
    service_account_email = module.params.get('service_account_email')
    if (external_ip == 'none'):
        instance_external_ip = None
    elif (external_ip != 'ephemeral'):
        instance_external_ip = external_ip
        try:
            try:
                socket.inet_aton(instance_external_ip)
                instance_external_ip = GCEAddress(id='unknown', name='unknown', address=instance_external_ip, region='unknown', driver=gce)
            except socket.error:
                instance_external_ip = gce.ex_get_address(instance_external_ip)
        except GoogleBaseError as e:
            module.fail_json(msg=('Unexpected error attempting to get a static ip %s, error: %s' % (external_ip, e.value)))
    else:
        instance_external_ip = external_ip
    new_instances = []
    changed = False
    lc_disks = []
    disk_modes = []
    for (i, disk) in enumerate((disks or [])):
        if isinstance(disk, dict):
            lc_disks.append(gce.ex_get_volume(disk['name'], lc_zone))
            disk_modes.append(disk['mode'])
        else:
            lc_disks.append(gce.ex_get_volume(disk, lc_zone))
            disk_modes.append(('READ_ONLY' if (i > 0) else 'READ_WRITE'))
    lc_network = gce.ex_get_network(network)
    lc_machine_type = gce.ex_get_size(machine_type, lc_zone)
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
    lc_image = LazyDiskImage(module, gce, image, lc_disks)
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
    if ((not lc_network) or (not lc_machine_type) or (not lc_zone)):
        module.fail_json(msg='Missing required create instance variable', changed=False)
    gce_args = dict(location=lc_zone, ex_network=network, ex_tags=tags, ex_metadata=metadata, ex_can_ip_forward=ip_forward, external_ip=instance_external_ip, ex_disk_auto_delete=disk_auto_delete, ex_service_accounts=ex_sa_perms)
    if (preemptible is not None):
        gce_args['ex_preemptible'] = preemptible
    if (subnetwork is not None):
        gce_args['ex_subnetwork'] = subnetwork
    if (isinstance(instance_names, str) and (not number)):
        instance_names = [instance_names]
    if (isinstance(instance_names, str) and number):
        instance_responses = gce.ex_create_multiple_nodes(instance_names, lc_machine_type, lc_image(), number, **gce_args)
        for resp in instance_responses:
            n = resp
            if isinstance(resp, libcloud.compute.drivers.gce.GCEFailedNode):
                try:
                    n = gce.ex_get_node(n.name, lc_zone)
                except ResourceNotFoundError:
                    pass
            else:
                changed = True
            new_instances.append(n)
    else:
        for instance in instance_names:
            pd = None
            if lc_disks:
                pd = lc_disks[0]
            elif persistent_boot_disk:
                try:
                    pd = gce.ex_get_volume(('%s' % instance), lc_zone)
                except ResourceNotFoundError:
                    pd = gce.create_volume(disk_size, ('%s' % instance), image=lc_image())
            gce_args['ex_boot_disk'] = pd
            inst = None
            try:
                inst = gce.ex_get_node(instance, lc_zone)
            except ResourceNotFoundError:
                inst = gce.create_node(instance, lc_machine_type, lc_image(), **gce_args)
                changed = True
            except GoogleBaseError as e:
                module.fail_json(msg=('Unexpected error attempting to create ' + ('instance %s, error: %s' % (instance, e.value))))
            if inst:
                new_instances.append(inst)
    for inst in new_instances:
        for (i, lc_disk) in enumerate(lc_disks):
            if (len(inst.extra['disks']) > i):
                attached_disk = inst.extra['disks'][i]
                if (attached_disk['source'] != lc_disk.extra['selfLink']):
                    module.fail_json(msg=('Disk at index %d does not match: requested=%s found=%s' % (i, lc_disk.extra['selfLink'], attached_disk['source'])))
                elif (attached_disk['mode'] != disk_modes[i]):
                    module.fail_json(msg=('Disk at index %d is in the wrong mode: requested=%s found=%s' % (i, disk_modes[i], attached_disk['mode'])))
                else:
                    continue
            gce.attach_volume(inst, lc_disk, ex_mode=disk_modes[i])
            if (len(inst.extra['disks']) != (i + 1)):
                inst.extra['disks'].append({
                    'source': lc_disk.extra['selfLink'],
                    'index': i,
                })
    instance_names = []
    instance_json_data = []
    for inst in new_instances:
        d = get_instance_info(inst)
        instance_names.append(d['name'])
        instance_json_data.append(d)
    return (changed, instance_json_data, instance_names)