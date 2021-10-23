def delete_oldest_non_default_version(iam, policy):
    versions = [v for v in iam.list_policy_versions(PolicyArn=policy['Arn'])['Versions'] if (not v['IsDefaultVersion'])]
    versions.sort(key=(lambda v: v['CreateDate']), reverse=True)
    for v in versions[(- 1):]:
        iam.delete_policy_version(PolicyArn=policy['Arn'], VersionId=v['VersionId'])