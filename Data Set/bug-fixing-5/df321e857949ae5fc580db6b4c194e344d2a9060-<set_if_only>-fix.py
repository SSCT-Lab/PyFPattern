def set_if_only(module, iam, policy, policy_version, is_only):
    if is_only:
        try:
            versions = [v for v in iam.list_policy_versions(PolicyArn=policy['Arn'])['Versions'] if (not v['IsDefaultVersion'])]
        except botocore.exceptions.ClientError as e:
            module.fail_json(msg=("Couldn't list policy versions: %s" % str(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        for v in versions:
            try:
                iam.delete_policy_version(PolicyArn=policy['Arn'], VersionId=v['VersionId'])
            except botocore.exceptions.ClientError as e:
                module.fail_json(msg=("Couldn't delete policy version: %s" % str(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        return (len(versions) > 0)
    return False