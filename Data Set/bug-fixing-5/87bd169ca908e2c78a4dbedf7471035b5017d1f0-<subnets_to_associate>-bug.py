def subnets_to_associate(nacl, client, module):
    params = list(module.params.get('subnets'))
    if (not params):
        return []
    if params[0].startswith('subnet-'):
        try:
            subnets = client.describe_subnets(Filters=[{
                'Name': 'subnet-id',
                'Values': params,
            }])
        except botocore.exceptions.ClientError as e:
            module.fail_json(msg=str(e))
    else:
        try:
            subnets = client.describe_subnets(Filters=[{
                'Name': 'tag:Name',
                'Values': params,
            }])
        except botocore.exceptions.ClientError as e:
            module.fail_json(msg=str(e))
    return [s['SubnetId'] for s in subnets['Subnets'] if s['SubnetId']]