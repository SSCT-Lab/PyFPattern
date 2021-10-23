def create_scaling_policy(connection, module):
    scaling_policy = connection.describe_scaling_policies(ServiceNamespace=module.params.get('service_namespace'), ResourceId=module.params.get('resource_id'), ScalableDimension=module.params.get('scalable_dimension'), PolicyNames=[module.params.get('policy_name')], MaxResults=1)
    changed = False
    if scaling_policy['ScalingPolicies']:
        scaling_policy = scaling_policy['ScalingPolicies'][0]
        for attr in ('PolicyName', 'ServiceNamespace', 'ResourceId', 'ScalableDimension', 'PolicyType', 'StepScalingPolicyConfiguration', 'TargetTrackingScalingPolicyConfiguration'):
            if ((attr in scaling_policy) and (scaling_policy[attr] != module.params.get(_camel_to_snake(attr)))):
                changed = True
                scaling_policy[attr] = module.params.get(_camel_to_snake(attr))
    else:
        changed = True
        scaling_policy = {
            'PolicyName': module.params.get('policy_name'),
            'ServiceNamespace': module.params.get('service_namespace'),
            'ResourceId': module.params.get('resource_id'),
            'ScalableDimension': module.params.get('scalable_dimension'),
            'PolicyType': module.params.get('policy_type'),
            'StepScalingPolicyConfiguration': module.params.get('step_scaling_policy_configuration'),
            'TargetTrackingScalingPolicyConfiguration': module.params.get('target_tracking_scaling_policy_configuration'),
        }
    if changed:
        try:
            if module.params.get('step_scaling_policy_configuration'):
                connection.put_scaling_policy(PolicyName=scaling_policy['PolicyName'], ServiceNamespace=scaling_policy['ServiceNamespace'], ResourceId=scaling_policy['ResourceId'], ScalableDimension=scaling_policy['ScalableDimension'], PolicyType=scaling_policy['PolicyType'], StepScalingPolicyConfiguration=scaling_policy['StepScalingPolicyConfiguration'])
            elif module.params.get('target_tracking_scaling_policy_configuration'):
                connection.put_scaling_policy(PolicyName=scaling_policy['PolicyName'], ServiceNamespace=scaling_policy['ServiceNamespace'], ResourceId=scaling_policy['ResourceId'], ScalableDimension=scaling_policy['ScalableDimension'], PolicyType=scaling_policy['PolicyType'], TargetTrackingScalingPolicyConfiguration=scaling_policy['TargetTrackingScalingPolicyConfiguration'])
        except Exception as e:
            module.fail_json(msg=str(e), exception=traceback.format_exc())
    try:
        response = connection.describe_scaling_policies(ServiceNamespace=module.params.get('service_namespace'), ResourceId=module.params.get('resource_id'), ScalableDimension=module.params.get('scalable_dimension'), PolicyNames=[module.params.get('policy_name')], MaxResults=1)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    if response['ScalingPolicies']:
        snaked_response = camel_dict_to_snake_dict(response['ScalingPolicies'][0])
    else:
        snaked_response = {
            
        }
    module.exit_json(changed=changed, response=snaked_response)