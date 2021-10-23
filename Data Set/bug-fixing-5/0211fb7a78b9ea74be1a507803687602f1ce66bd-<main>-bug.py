def main():
    global module
    module = AnsibleModule(argument_spec=dict(name=dict(type='str', required=True, aliases=['volume']), state=dict(type='str', required=True, choices=['absent', 'started', 'stopped', 'present']), cluster=dict(type='list'), host=dict(type='str'), stripes=dict(type='int'), replicas=dict(type='int'), arbiters=dict(type='int'), disperses=dict(type='int'), redundancies=dict(type='int'), transport=dict(type='str', default='tcp', choices=['tcp', 'rdma', 'tcp,rdma']), bricks=dict(type='str', aliases=['brick']), start_on_create=dict(type='bool', default=True), rebalance=dict(type='bool', default=False), options=dict(type='dict', default={
        
    }), quota=dict(type='str'), directory=dict(type='str'), force=dict(type='bool', default=False)))
    global glusterbin
    glusterbin = module.get_bin_path('gluster', True)
    changed = False
    action = module.params['state']
    volume_name = module.params['name']
    cluster = module.params['cluster']
    brick_paths = module.params['bricks']
    stripes = module.params['stripes']
    replicas = module.params['replicas']
    arbiters = module.params['arbiters']
    disperses = module.params['disperses']
    redundancies = module.params['redundancies']
    transport = module.params['transport']
    myhostname = module.params['host']
    start_on_create = module.boolean(module.params['start_on_create'])
    rebalance = module.boolean(module.params['rebalance'])
    force = module.boolean(module.params['force'])
    if (not myhostname):
        myhostname = socket.gethostname()
    if ((cluster is not None) and (len(cluster) > 1) and (cluster[(- 1)] == '')):
        cluster = cluster[0:(- 1)]
    if ((cluster is None) or (cluster[0] == '')):
        cluster = [myhostname]
    if ((brick_paths is not None) and (',' in brick_paths)):
        brick_paths = brick_paths.split(',')
    else:
        brick_paths = [brick_paths]
    options = module.params['options']
    quota = module.params['quota']
    directory = module.params['directory']
    peers = get_peers()
    volumes = get_volumes()
    quotas = {
        
    }
    if ((volume_name in volumes) and volumes[volume_name]['quota'] and (volumes[volume_name]['status'].lower() == 'started')):
        quotas = get_quotas(volume_name, True)
    if (action == 'absent'):
        if (volume_name in volumes):
            if (volumes[volume_name]['status'].lower() != 'stopped'):
                stop_volume(volume_name)
            run_gluster(['volume', 'delete', volume_name])
            changed = True
    if (action == 'present'):
        probe_all_peers(cluster, peers, myhostname)
        if (volume_name not in volumes):
            create_volume(volume_name, stripes, replicas, arbiters, disperses, redundancies, transport, cluster, brick_paths, force)
            volumes = get_volumes()
            changed = True
        if (volume_name in volumes):
            if ((volumes[volume_name]['status'].lower() != 'started') and start_on_create):
                start_volume(volume_name)
                changed = True
            new_bricks = []
            removed_bricks = []
            all_bricks = []
            for node in cluster:
                for brick_path in brick_paths:
                    brick = ('%s:%s' % (node, brick_path))
                    all_bricks.append(brick)
                    if (brick not in volumes[volume_name]['bricks']):
                        new_bricks.append(brick)
            for brick in volumes[volume_name]['bricks']:
                if (brick not in all_bricks):
                    removed_bricks.append(brick)
            if new_bricks:
                add_bricks(volume_name, new_bricks, stripes, replicas, force)
                changed = True
            if quota:
                if (not volumes[volume_name]['quota']):
                    enable_quota(volume_name)
                quotas = get_quotas(volume_name, False)
                if ((directory not in quotas) or (quotas[directory] != quota)):
                    set_quota(volume_name, directory, quota)
                    changed = True
            for option in options.keys():
                if ((option not in volumes[volume_name]['options']) or (volumes[volume_name]['options'][option] != options[option])):
                    set_volume_option(volume_name, option, options[option])
                    changed = True
        else:
            module.fail_json(msg=('failed to create volume %s' % volume_name))
    if ((action != 'delete') and (volume_name not in volumes)):
        module.fail_json(msg=('volume not found %s' % volume_name))
    if (action == 'started'):
        if (volumes[volume_name]['status'].lower() != 'started'):
            start_volume(volume_name)
            changed = True
    if (action == 'stopped'):
        if (volumes[volume_name]['status'].lower() != 'stopped'):
            stop_volume(volume_name)
            changed = True
    if changed:
        volumes = get_volumes()
        if rebalance:
            do_rebalance(volume_name)
    facts = {
        
    }
    facts['glusterfs'] = {
        'peers': peers,
        'volumes': volumes,
        'quotas': quotas,
    }
    module.exit_json(changed=changed, ansible_facts=facts)