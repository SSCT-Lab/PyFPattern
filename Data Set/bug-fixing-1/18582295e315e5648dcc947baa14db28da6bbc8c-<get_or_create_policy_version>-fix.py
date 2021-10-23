

def get_or_create_policy_version(module, iam, policy, policy_document):
    try:
        versions = iam.list_policy_versions(PolicyArn=policy['Arn'])['Versions']
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=("Couldn't list policy versions: %s" % str(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    for v in versions:
        try:
            document = iam.get_policy_version(PolicyArn=policy['Arn'], VersionId=v['VersionId'])['PolicyVersion']['Document']
        except botocore.exceptions.ClientError as e:
            module.fail_json(msg=("Couldn't get policy version %s: %s" % (v['VersionId'], str(e))), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
        if (sort_json_policy_dict(document) == sort_json_policy_dict(json.loads(policy_document))):
            return (v, False)
    try:
        version = iam.create_policy_version(PolicyArn=policy['Arn'], PolicyDocument=policy_document)['PolicyVersion']
        return (version, True)
    except botocore.exceptions.ClientError as e:
        if (e.response['Error']['Code'] == 'LimitExceeded'):
            delete_oldest_non_default_version(module, iam, policy)
            try:
                version = iam.create_policy_version(PolicyArn=policy['Arn'], PolicyDocument=policy_document)['PolicyVersion']
                return (version, True)
            except botocore.exceptions.ClientError as e:
                pass
        module.fail_json(msg=("Couldn't create policy version: %s" % str(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
