def _hashable_policy(policy, policy_list):
    "\n        Takes a policy and returns a list, the contents of which are all hashable and sorted.\n        Example input policy:\n        {'Version': '2012-10-17',\n         'Statement': [{'Action': 's3:PutObjectAcl',\n                        'Sid': 'AddCannedAcl2',\n                        'Resource': 'arn:aws:s3:::test_policy/*',\n                        'Effect': 'Allow',\n                        'Principal': {'AWS': ['arn:aws:iam::XXXXXXXXXXXX:user/username1', 'arn:aws:iam::XXXXXXXXXXXX:user/username2']}\n                       }]}\n        Returned value:\n        [('Statement',  ((('Action', (u's3:PutObjectAcl',)),\n                          ('Effect', (u'Allow',)),\n                          ('Principal', ('AWS', ((u'arn:aws:iam::XXXXXXXXXXXX:user/username1',), (u'arn:aws:iam::XXXXXXXXXXXX:user/username2',)))),\n                          ('Resource', (u'arn:aws:s3:::test_policy/*',)), ('Sid', (u'AddCannedAcl2',)))),\n         ('Version', (u'2012-10-17',)))]\n\n    "
    if isinstance(policy, list):
        for each in policy:
            tupleified = _hashable_policy(each, [])
            if isinstance(tupleified, list):
                tupleified = tuple(tupleified)
            policy_list.append(tupleified)
    elif (isinstance(policy, string_types) or isinstance(policy, binary_type)):
        if (policy.startswith('arn:aws:iam::') and policy.endswith(':root')):
            policy = policy.split(':')[4]
        return [to_text(policy)]
    elif isinstance(policy, dict):
        sorted_keys = list(policy.keys())
        sorted_keys.sort()
        for key in sorted_keys:
            tupleified = _hashable_policy(policy[key], [])
            if isinstance(tupleified, list):
                tupleified = tuple(tupleified)
            policy_list.append((key, tupleified))
    if ((len(policy_list) == 1) and isinstance(policy_list[0], tuple)):
        policy_list = policy_list[0]
    if isinstance(policy_list, list):
        if PY3_COMPARISON:
            policy_list.sort(key=cmp_to_key(py3cmp))
        else:
            policy_list.sort()
    return policy_list