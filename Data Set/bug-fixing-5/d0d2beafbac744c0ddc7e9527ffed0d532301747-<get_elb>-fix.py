def get_elb(connection, module):
    '\n    Get an application load balancer based on name. If not found, return None\n\n    :param connection: ELBv2 boto3 connection\n    :param module: Ansible module object\n    :return: Dict of load balancer attributes or None if not found\n    '
    try:
        load_balancer_paginator = connection.get_paginator('describe_load_balancers')
        return load_balancer_paginator.paginate(Names=[module.params.get('name')]).build_full_result()['LoadBalancers'][0]
    except ClientError as e:
        if (e.response['Error']['Code'] == 'LoadBalancerNotFound'):
            return None
        else:
            module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))