def detach_all_entities(iam, policy, **kwargs):
    entities = iam.list_entities_for_policy(PolicyArn=policy['Arn'], **kwargs)
    for g in entities['PolicyGroups']:
        iam.detach_group_policy(PolicyArn=policy['Arn'], GroupName=g['GroupName'])
    for u in entities['PolicyUsers']:
        iam.detach_user_policy(PolicyArn=policy['Arn'], UserName=u['UserName'])
    for r in entities['PolicyRoles']:
        iam.detach_role_policy(PolicyArn=policy['Arn'], RoleName=r['RoleName'])
    if entities['IsTruncated']:
        detach_all_entities(iam, policy, marker=entities['Marker'])