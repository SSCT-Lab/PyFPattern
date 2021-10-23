def detach_all_entities(module, iam, policy, **kwargs):
    try:
        entities = iam.list_entities_for_policy(PolicyArn=policy['Arn'], **kwargs)
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=("Couldn't detach list entities for policy %s: %s" % (policy['PolicyName'], str(e))), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    for g in entities['PolicyGroups']:
        try:
            iam.detach_group_policy(PolicyArn=policy['Arn'], GroupName=g['GroupName'])
        except botocore.exceptions.ClientError as e:
            module.fail_json(msg=("Couldn't detach group policy %s: %s" % (g['GroupName'], str(e))), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    for u in entities['PolicyUsers']:
        try:
            iam.detach_user_policy(PolicyArn=policy['Arn'], UserName=u['UserName'])
        except botocore.exceptions.ClientError as e:
            module.fail_json(msg=("Couldn't detach user policy %s: %s" % (u['UserName'], str(e))), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    for r in entities['PolicyRoles']:
        try:
            iam.detach_role_policy(PolicyArn=policy['Arn'], RoleName=r['RoleName'])
        except botocore.exceptions.ClientError as e:
            module.fail_json(msg=("Couldn't detach role policy %s: %s" % (r['RoleName'], str(e))), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    if entities['IsTruncated']:
        detach_all_entities(module, iam, policy, marker=entities['Marker'])