def _list_into_cache(regions):
    groups = collections.defaultdict(list)
    hostvars = collections.defaultdict(dict)
    images = {
        
    }
    cbs_attachments = collections.defaultdict(dict)
    prefix = get_config(p, 'rax', 'meta_prefix', 'RAX_META_PREFIX', 'meta')
    try:
        networks = get_config(p, 'rax', 'access_network', 'RAX_ACCESS_NETWORK', 'public', value_type='list')
    except TypeError:
        networks = get_config(p, 'rax', 'access_network', 'RAX_ACCESS_NETWORK', 'public', islist=True)
    try:
        try:
            ip_versions = map(int, get_config(p, 'rax', 'access_ip_version', 'RAX_ACCESS_IP_VERSION', 4, value_type='list'))
        except TypeError:
            ip_versions = map(int, get_config(p, 'rax', 'access_ip_version', 'RAX_ACCESS_IP_VERSION', 4, islist=True))
    except:
        ip_versions = [4]
    else:
        ip_versions = [v for v in ip_versions if (v in [4, 6])]
        if (not ip_versions):
            ip_versions = [4]
    for region in regions:
        cs = pyrax.connect_to_cloudservers(region=region)
        if (cs is None):
            warnings.warn(('Connecting to Rackspace region "%s" has caused Pyrax to return None. Is this a valid region?' % region), RuntimeWarning)
            continue
        for server in cs.servers.list():
            groups[region].append(server.name)
            group = server.metadata.get('group')
            if group:
                groups[group].append(server.name)
            for extra_group in server.metadata.get('groups', '').split(','):
                if extra_group:
                    groups[extra_group].append(server.name)
            for (key, value) in to_dict(server).items():
                hostvars[server.name][key] = value
            hostvars[server.name]['rax_region'] = region
            for (key, value) in iteritems(server.metadata):
                groups[('%s_%s_%s' % (prefix, key, value))].append(server.name)
            groups[('instance-%s' % server.id)].append(server.name)
            groups[('flavor-%s' % server.flavor['id'])].append(server.name)
            if (not server.image):
                if (not cbs_attachments[region]):
                    cbs = pyrax.connect_to_cloud_blockstorage(region)
                    for vol in cbs.list():
                        if mk_boolean(vol.bootable):
                            for attachment in vol.attachments:
                                metadata = vol.volume_image_metadata
                                server_id = attachment['server_id']
                                cbs_attachments[region][server_id] = {
                                    'id': metadata['image_id'],
                                    'name': slugify(metadata['image_name']),
                                }
                image = cbs_attachments[region].get(server.id)
                if image:
                    server.image = {
                        'id': image['id'],
                    }
                    hostvars[server.name]['rax_image'] = server.image
                    hostvars[server.name]['rax_boot_source'] = 'volume'
                    images[image['id']] = image['name']
            else:
                hostvars[server.name]['rax_boot_source'] = 'local'
            try:
                imagegroup = ('image-%s' % images[server.image['id']])
                groups[imagegroup].append(server.name)
                groups[('image-%s' % server.image['id'])].append(server.name)
            except KeyError:
                try:
                    image = cs.images.get(server.image['id'])
                except cs.exceptions.NotFound:
                    groups[('image-%s' % server.image['id'])].append(server.name)
                else:
                    images[image.id] = image.human_id
                    groups[('image-%s' % image.human_id)].append(server.name)
                    groups[('image-%s' % server.image['id'])].append(server.name)
            ansible_ssh_host = None
            for network_name in networks:
                if ansible_ssh_host:
                    break
                if (network_name == 'public'):
                    for version_name in ip_versions:
                        if ansible_ssh_host:
                            break
                        if ((version_name == 6) and server.accessIPv6):
                            ansible_ssh_host = server.accessIPv6
                        elif server.accessIPv4:
                            ansible_ssh_host = server.accessIPv4
                if (not ansible_ssh_host):
                    addresses = server.addresses.get(network_name, [])
                    for address in addresses:
                        for version_name in ip_versions:
                            if ansible_ssh_host:
                                break
                            if (address.get('version') == version_name):
                                ansible_ssh_host = address.get('addr')
                                break
            if ansible_ssh_host:
                hostvars[server.name]['ansible_ssh_host'] = ansible_ssh_host
    if hostvars:
        groups['_meta'] = {
            'hostvars': hostvars,
        }
    with open(get_cache_file_path(regions), 'w') as cache_file:
        json.dump(groups, cache_file)