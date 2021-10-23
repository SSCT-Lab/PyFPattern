def delete_oldest_non_default_version(module, iam, policy):
    try:
        versions = [v for v in iam.list_policy_versions(PolicyArn=policy['Arn'])['Versions'] if (not v['IsDefaultVersion'])]
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=("Couldn't list policy versions: %s" % str(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    versions.sort(key=(lambda v: v['CreateDate']), reverse=True)
    for v in versions[(- 1):]:
        try:
            iam.delete_policy_version(PolicyArn=policy['Arn'], VersionId=v['VersionId'])
        except botocore.exceptions.ClientError as e:
            module.fail_json(msg=("Couldn't delete policy version: %s" % str(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))