

def list_target_groups(connection, module):
    load_balancer_arn = module.params.get('load_balancer_arn')
    target_group_arns = module.params.get('target_group_arns')
    names = module.params.get('names')
    try:
        target_group_paginator = connection.get_paginator('describe_target_groups')
        if ((not load_balancer_arn) and (not target_group_arns) and (not names)):
            target_groups = target_group_paginator.paginate().build_full_result()
        if load_balancer_arn:
            target_groups = target_group_paginator.paginate(LoadBalancerArn=load_balancer_arn).build_full_result()
        if target_group_arns:
            target_groups = target_group_paginator.paginate(TargetGroupArns=target_group_arns).build_full_result()
        if names:
            target_groups = target_group_paginator.paginate(Names=names).build_full_result()
    except ClientError as e:
        if (e.response['Error']['Code'] == 'TargetGroupNotFound'):
            module.exit_json(target_groups=[])
        else:
            module.fail_json(msg=e.message, exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    except NoCredentialsError as e:
        module.fail_json(msg=('AWS authentication problem. ' + e.message), exception=traceback.format_exc())
    for target_group in target_groups['TargetGroups']:
        target_group.update(get_target_group_attributes(connection, module, target_group['TargetGroupArn']))
        target_group['tags'] = get_target_group_tags(connection, module, target_group['TargetGroupArn'])
    snaked_target_groups = [camel_dict_to_snake_dict(target_group) for target_group in target_groups['TargetGroups']]
    module.exit_json(target_groups=snaked_target_groups)
