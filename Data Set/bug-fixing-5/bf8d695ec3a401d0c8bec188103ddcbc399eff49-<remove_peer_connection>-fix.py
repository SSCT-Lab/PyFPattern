def remove_peer_connection(client, module):
    pcx_id = module.params.get('peering_id')
    if (not pcx_id):
        params = dict()
        params['VpcId'] = module.params.get('vpc_id')
        params['PeerVpcId'] = module.params.get('peer_vpc_id')
        params['PeerRegion'] = module.params.get('peer_region')
        if module.params.get('peer_owner_id'):
            params['PeerOwnerId'] = str(module.params.get('peer_owner_id'))
        peering_conns = describe_peering_connections(params, client)
        if (not peering_conns):
            module.exit_json(changed=False)
        else:
            pcx_id = peering_conns['VpcPeeringConnections'][0]['VpcPeeringConnectionId']
    try:
        params = dict()
        params['VpcPeeringConnectionId'] = pcx_id
        client.delete_vpc_peering_connection(**params)
        module.exit_json(changed=True)
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=str(e))