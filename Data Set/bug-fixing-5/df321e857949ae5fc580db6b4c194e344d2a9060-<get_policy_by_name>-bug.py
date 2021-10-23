def get_policy_by_name(iam, name, **kwargs):
    response = iam.list_policies(Scope='Local', **kwargs)
    for policy in response['Policies']:
        if (policy['PolicyName'] == name):
            return policy
    if response['IsTruncated']:
        return get_policy_by_name(iam, name, marker=response['marker'])
    return None