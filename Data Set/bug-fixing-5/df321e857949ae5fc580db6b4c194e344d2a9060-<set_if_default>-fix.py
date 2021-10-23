def set_if_default(module, iam, policy, policy_version, is_default):
    if (is_default and (not policy_version['IsDefaultVersion'])):
        try:
            iam.set_default_policy_version(PolicyArn=policy['Arn'], VersionId=policy_version['VersionId'])
        except botocore.exceptions.ClientError as e:
            module.fail_json(msg=("Couldn't set default policy version: %s" % str(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        return True
    return False