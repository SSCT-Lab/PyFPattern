def create(client, subnet_id, allocation_id, client_token=None, wait=False, wait_timeout=0, if_exist_do_not_create=False, check_mode=False):
    'Create an Amazon NAT Gateway.\n    Args:\n        client (botocore.client.EC2): Boto3 client\n        subnet_id (str): The subnet_id the nat resides in.\n        allocation_id (str): The eip Amazon identifier.\n\n    Kwargs:\n        if_exist_do_not_create (bool): if a nat gateway already exists in this\n            subnet, than do not create another one.\n            default = False\n        wait (bool): Wait for the nat to be in the deleted state before returning.\n            default = False\n        wait_timeout (int): Number of seconds to wait, until this timeout is reached.\n            default = 0\n        client_token (str):\n            default = None\n\n    Basic Usage:\n        >>> client = boto3.client(\'ec2\')\n        >>> subnet_id = \'subnet-1234567\'\n        >>> allocation_id = \'eipalloc-1234567\'\n        >>> create(client, subnet_id, allocation_id, if_exist_do_not_create=True, wait=True, wait_timeout=500)\n        [\n            true,\n            "",\n            {\n                "nat_gateway_id": "nat-123456789",\n                "subnet_id": "subnet-1234567",\n                "nat_gateway_addresses": [\n                    {\n                        "public_ip": "55.55.55.55",\n                        "network_interface_id": "eni-1234567",\n                        "private_ip": "10.0.0.102",\n                        "allocation_id": "eipalloc-1234567"\n                    }\n                ],\n                "state": "deleted",\n                "create_time": "2016-03-05T00:33:21.209000+00:00",\n                "delete_time": "2016-03-05T00:36:37.329000+00:00",\n                "vpc_id": "vpc-1234567"\n            }\n        ]\n\n    Returns:\n        Tuple (bool, str, list)\n    '
    params = {
        'SubnetId': subnet_id,
        'AllocationId': allocation_id,
    }
    request_time = datetime.datetime.utcnow()
    changed = False
    success = False
    token_provided = False
    err_msg = ''
    if client_token:
        token_provided = True
        params['ClientToken'] = client_token
    try:
        if (not check_mode):
            result = camel_dict_to_snake_dict(client.create_nat_gateway(**params)['NatGateway'])
        else:
            result = DRY_RUN_GATEWAYS[0]
            result['create_time'] = datetime.datetime.utcnow()
            result['nat_gateway_addresses'][0]['Allocation_id'] = allocation_id
            result['subnet_id'] = subnet_id
        success = True
        changed = True
        create_time = result['create_time'].replace(tzinfo=None)
        if (token_provided and (request_time > create_time)):
            changed = False
        elif wait:
            (success, err_msg, result) = wait_for_status(client, wait_timeout, result['nat_gateway_id'], 'available', check_mode=check_mode)
            if success:
                err_msg = 'NAT gateway {0} created'.format(result['nat_gateway_id'])
    except botocore.exceptions.ClientError as e:
        if ('IdempotentParameterMismatch' in e.message):
            err_msg = ('NAT Gateway does not support update and token has already been provided: ' + str(e))
        else:
            err_msg = str(e)
        success = False
        changed = False
        result = None
    return (success, changed, err_msg, result)