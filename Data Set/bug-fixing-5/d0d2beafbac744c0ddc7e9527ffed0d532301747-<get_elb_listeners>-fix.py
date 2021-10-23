def get_elb_listeners(connection, module, elb_arn):
    try:
        listener_paginator = connection.get_paginator('describe_listeners')
        return listener_paginator.paginate(LoadBalancerArn=elb_arn).build_full_result()['Listeners']
    except ClientError as e:
        module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))