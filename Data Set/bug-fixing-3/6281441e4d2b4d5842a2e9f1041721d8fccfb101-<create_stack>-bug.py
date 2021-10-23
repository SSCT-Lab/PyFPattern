def create_stack(module, stack_params, cfn):
    if (('TemplateBody' not in stack_params) and ('TemplateURL' not in stack_params)):
        module.fail_json(msg="Either 'template', 'template_body' or 'template_url' is required when the stack does not exist.")
    stack_params['DisableRollback'] = module.params['disable_rollback']
    if (module.params.get('termination_protection') is not None):
        if boto_supports_termination_protection(cfn):
            stack_params['EnableTerminationProtection'] = bool(module.params.get('termination_protection'))
        else:
            module.fail_json(msg='termination_protection parameter requires botocore >= 1.7.18')
    try:
        cfn.create_stack(**stack_params)
        result = stack_operation(cfn, stack_params['StackName'], 'CREATE', stack_params.get('ClientRequestToken', None))
    except Exception as err:
        error_msg = boto_exception(err)
        module.fail_json(msg='Failed to create stack {0}: {1}.'.format(stack_params.get('StackName'), error_msg), exception=traceback.format_exc())
    if (not result):
        module.fail_json(msg='empty result')
    return result