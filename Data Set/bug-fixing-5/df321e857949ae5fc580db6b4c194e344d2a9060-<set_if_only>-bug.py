def set_if_only(iam, policy, policy_version, is_only):
    if is_only:
        versions = [v for v in iam.list_policy_versions(PolicyArn=policy['Arn'])['Versions'] if (not v['IsDefaultVersion'])]
        for v in versions:
            iam.delete_policy_version(PolicyArn=policy['Arn'], VersionId=v['VersionId'])
        return (len(versions) > 0)
    return False