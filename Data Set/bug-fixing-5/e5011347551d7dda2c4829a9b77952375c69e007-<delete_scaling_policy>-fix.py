def delete_scaling_policy(connection, module):
    changed = False
    try:
        scaling_policy = connection.describe_scaling_policies(ServiceNamespace=module.params.get('service_namespace'), ResourceId=module.params.get('resource_id'), ScalableDimension=module.params.get('scalable_dimension'), PolicyNames=[module.params.get('policy_name')], MaxResults=1)
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        module.fail_json_aws(e, msg='Failed to describe scaling policies')
    if scaling_policy['ScalingPolicies']:
        try:
            connection.delete_scaling_policy(ServiceNamespace=module.params.get('service_namespace'), ResourceId=module.params.get('resource_id'), ScalableDimension=module.params.get('scalable_dimension'), PolicyName=module.params.get('policy_name'))
            changed = True
        except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
            module.fail_json_aws(e, msg='Failed to delete scaling policy')
    return {
        'changed': changed,
    }