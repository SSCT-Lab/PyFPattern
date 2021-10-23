def get_policy_by_name(module, iam, name):
    try:
        response = list_policies_with_backoff(iam)
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=("Couldn't list policies: %s" % str(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    for policy in response['Policies']:
        if (policy['PolicyName'] == name):
            return policy
    return None