def accept_reject(state, client, module):
    changed = False
    params = dict()
    params['VpcPeeringConnectionId'] = module.params.get('peering_id')
    params['DryRun'] = module.check_mode
    if (peer_status(client, module) != 'active'):
        try:
            if (state == 'accept'):
                client.accept_vpc_peering_connection(**params)
            else:
                client.reject_vpc_peering_connection(**params)
            if module.params.get('tags'):
                create_tags(params['VpcPeeringConnectionId'], client, module)
            changed = True
        except botocore.exceptions.ClientError as e:
            module.fail_json(msg=str(e))
    if tags_changed(params['VpcPeeringConnectionId'], client, module):
        changed = True
    return (changed, params['VpcPeeringConnectionId'])