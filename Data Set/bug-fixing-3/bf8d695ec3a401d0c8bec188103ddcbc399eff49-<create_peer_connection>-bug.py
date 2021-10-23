def create_peer_connection(client, module):
    changed = False
    params = dict()
    params['VpcId'] = module.params.get('vpc_id')
    params['PeerVpcId'] = module.params.get('peer_vpc_id')
    if module.params.get('peer_region'):
        if (distutils.version.StrictVersion(botocore.__version__) < distutils.version.StrictVersion('1.8.6')):
            module.fail_json(msg='specifying peer_region parameter requires botocore >= 1.8.6')
        params['PeerRegion'] = module.params.get('peer_region')
    if module.params.get('peer_owner_id'):
        params['PeerOwnerId'] = str(module.params.get('peer_owner_id'))
    params['DryRun'] = module.check_mode
    peering_conns = describe_peering_connections(params, client)
    for peering_conn in peering_conns['VpcPeeringConnections']:
        pcx_id = peering_conn['VpcPeeringConnectionId']
        if tags_changed(pcx_id, client, module):
            changed = True
        if is_active(peering_conn):
            return (changed, peering_conn['VpcPeeringConnectionId'])
        if is_pending(peering_conn):
            return (changed, peering_conn['VpcPeeringConnectionId'])
    try:
        peering_conn = client.create_vpc_peering_connection(**params)
        pcx_id = peering_conn['VpcPeeringConnection']['VpcPeeringConnectionId']
        if module.params.get('tags'):
            create_tags(pcx_id, client, module)
        changed = True
        return (changed, peering_conn['VpcPeeringConnection']['VpcPeeringConnectionId'])
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=str(e))