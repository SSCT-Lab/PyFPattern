def delete_scaling_policy(connection, module):
    changed = False
    scaling_policy = connection.describe_scaling_policies(ServiceNamespace=module.params.get('service_namespace'), ResourceId=module.params.get('resource_id'), ScalableDimension=module.params.get('scalable_dimension'), PolicyNames=[module.params.get('policy_name')], MaxResults=1)
    if scaling_policy['ScalingPolicies']:
        try:
            connection.delete_scaling_policy(ServiceNamespace=module.params.get('service_namespace'), ResourceId=module.params.get('resource_id'), ScalableDimension=module.params.get('scalable_dimension'), PolicyName=module.params.get('policy_name'))
            changed = True
        except Exception as e:
            module.fail_json(msg=str(e), exception=traceback.format_exc())
    module.exit_json(changed=changed)