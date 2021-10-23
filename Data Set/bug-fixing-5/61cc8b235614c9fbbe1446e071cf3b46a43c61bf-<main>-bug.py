def main():
    argument_spec = ansible.module_utils.ec2.ec2_argument_spec()
    argument_spec.update(dict(stack_name=dict(required=True), template_parameters=dict(required=False, type='dict', default={
        
    }), state=dict(default='present', choices=['present', 'absent']), template=dict(default=None, required=False, type='path'), notification_arns=dict(default=None, required=False), stack_policy=dict(default=None, required=False), disable_rollback=dict(default=False, type='bool'), template_url=dict(default=None, required=False), template_format=dict(default=None, choices=['json', 'yaml'], required=False), create_changeset=dict(default=False, type='bool'), changeset_name=dict(default=None, required=False), role_arn=dict(default=None, required=False), tags=dict(default=None, type='dict'), termination_protection=dict(default=None, type='bool')))
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=[['template_url', 'template']], supports_check_mode=True)
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 and botocore are required for this module')
    stack_params = {
        'Capabilities': ['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
        'ClientRequestToken': to_native(uuid.uuid4()),
    }
    state = module.params['state']
    stack_params['StackName'] = module.params['stack_name']
    if (module.params['template'] is not None):
        stack_params['TemplateBody'] = open(module.params['template'], 'r').read()
    elif (module.params['template_url'] is not None):
        stack_params['TemplateURL'] = module.params['template_url']
    if module.params.get('notification_arns'):
        stack_params['NotificationARNs'] = module.params['notification_arns'].split(',')
    else:
        stack_params['NotificationARNs'] = []
    if ((module.params['stack_policy'] is not None) and (not module.check_mode)):
        stack_params['StackPolicyBody'] = open(module.params['stack_policy'], 'r').read()
    template_parameters = module.params['template_parameters']
    stack_params['Parameters'] = [{
        'ParameterKey': k,
        'ParameterValue': str(v),
    } for (k, v) in template_parameters.items()]
    if isinstance(module.params.get('tags'), dict):
        stack_params['Tags'] = ansible.module_utils.ec2.ansible_dict_to_boto3_tag_list(module.params['tags'])
    if module.params.get('role_arn'):
        stack_params['RoleARN'] = module.params['role_arn']
    result = {
        
    }
    try:
        (region, ec2_url, aws_connect_kwargs) = ansible.module_utils.ec2.get_aws_connection_info(module, boto3=True)
        cfn = ansible.module_utils.ec2.boto3_conn(module, conn_type='client', resource='cloudformation', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except botocore.exceptions.NoCredentialsError as e:
        module.fail_json(msg=boto_exception(e))
    backoff_wrapper = AWSRetry.jittered_backoff(retries=10, delay=3, max_delay=30)
    cfn.describe_stack_events = backoff_wrapper(cfn.describe_stack_events)
    cfn.create_stack = backoff_wrapper(cfn.create_stack)
    cfn.list_change_sets = backoff_wrapper(cfn.list_change_sets)
    cfn.create_change_set = backoff_wrapper(cfn.create_change_set)
    cfn.update_stack = backoff_wrapper(cfn.update_stack)
    cfn.describe_stacks = backoff_wrapper(cfn.describe_stacks)
    cfn.list_stack_resources = backoff_wrapper(cfn.list_stack_resources)
    cfn.delete_stack = backoff_wrapper(cfn.delete_stack)
    if boto_supports_termination_protection(cfn):
        cfn.update_termination_protection = backoff_wrapper(cfn.update_termination_protection)
    stack_info = get_stack_facts(cfn, stack_params['StackName'])
    if module.check_mode:
        if ((state == 'absent') and stack_info):
            module.exit_json(changed=True, msg='Stack would be deleted', meta=[])
        elif ((state == 'absent') and (not stack_info)):
            module.exit_json(changed=False, msg="Stack doesn't exist", meta=[])
        elif ((state == 'present') and (not stack_info)):
            module.exit_json(changed=True, msg='New stack would be created', meta=[])
        else:
            module.exit_json(**check_mode_changeset(module, stack_params, cfn))
    if (state == 'present'):
        if (not stack_info):
            result = create_stack(module, stack_params, cfn)
        elif module.params.get('create_changeset'):
            result = create_changeset(module, stack_params, cfn)
        else:
            if (module.params.get('termination_protection') is not None):
                update_termination_protection(module, cfn, stack_params['StackName'], bool(module.params.get('termination_protection')))
            result = update_stack(module, stack_params, cfn)
        stack = get_stack_facts(cfn, stack_params['StackName'])
        if (result.get('stack_outputs') is None):
            result['stack_outputs'] = {
                
            }
        for output in stack.get('Outputs', []):
            result['stack_outputs'][output['OutputKey']] = output['OutputValue']
        stack_resources = []
        reslist = cfn.list_stack_resources(StackName=stack_params['StackName'])
        for res in reslist.get('StackResourceSummaries', []):
            stack_resources.append({
                'logical_resource_id': res['LogicalResourceId'],
                'physical_resource_id': res.get('PhysicalResourceId', ''),
                'resource_type': res['ResourceType'],
                'last_updated_time': res['LastUpdatedTimestamp'],
                'status': res['ResourceStatus'],
                'status_reason': res.get('ResourceStatusReason'),
            })
        result['stack_resources'] = stack_resources
    elif (state == 'absent'):
        try:
            stack = get_stack_facts(cfn, stack_params['StackName'])
            if (not stack):
                result = {
                    'changed': False,
                    'output': 'Stack not found.',
                }
            else:
                cfn.delete_stack(StackName=stack_params['StackName'])
                result = stack_operation(cfn, stack_params['StackName'], 'DELETE', stack_params.get('ClientRequestToken', None))
        except Exception as err:
            module.fail_json(msg=boto_exception(err), exception=traceback.format_exc())
    if (module.params['template_format'] is not None):
        result['warnings'] = ['Argument `template_format` is deprecated since Ansible 2.3, JSON and YAML templates are now passed directly to the CloudFormation API.']
    module.exit_json(**result)