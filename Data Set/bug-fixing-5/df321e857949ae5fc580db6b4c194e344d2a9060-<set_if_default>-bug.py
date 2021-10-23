def set_if_default(iam, policy, policy_version, is_default):
    if (is_default and (not policy_version['IsDefaultVersion'])):
        iam.set_default_policy_version(PolicyArn=policy['Arn'], VersionId=policy_version['VersionId'])
        return True
    return False