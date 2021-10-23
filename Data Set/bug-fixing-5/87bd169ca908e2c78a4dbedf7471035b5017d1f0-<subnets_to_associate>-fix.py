def subnets_to_associate(nacl, client, module):
    params = list(module.params.get('subnets'))
    if (not params):
        return []
    all_found = []
    if any((x.startswith('subnet-') for x in params)):
        try:
            subnets = client.describe_subnets(Filters=[{
                'Name': 'subnet-id',
                'Values': params,
            }])
            all_found.extend(subnets.get('Subnets', []))
        except botocore.exceptions.ClientError as e:
            module.fail_json(msg=str(e), exception=traceback.format_exc())
    if (len(params) != len(all_found)):
        try:
            subnets = client.describe_subnets(Filters=[{
                'Name': 'tag:Name',
                'Values': params,
            }])
            all_found.extend(subnets.get('Subnets', []))
        except botocore.exceptions.ClientError as e:
            module.fail_json(msg=str(e), exception=traceback.format_exc())
    return list(set((s['SubnetId'] for s in all_found if s.get('SubnetId'))))