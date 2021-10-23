def get_or_create_policy_version(iam, policy, policy_document):
    versions = iam.list_policy_versions(PolicyArn=policy['Arn'])['Versions']
    for v in versions:
        document = iam.get_policy_version(PolicyArn=policy['Arn'], VersionId=v['VersionId'])['PolicyVersion']['Document']
        if (sort_json_policy_dict(document) == sort_json_policy_dict(json.loads(policy_document))):
            return (v, False)
    try:
        return (iam.create_policy_version(PolicyArn=policy['Arn'], PolicyDocument=policy_document)['PolicyVersion'], True)
    except Exception as e:
        delete_oldest_non_default_version(iam, policy)
        return (iam.create_policy_version(PolicyArn=policy['Arn'], PolicyDocument=policy_document)['PolicyVersion'], True)