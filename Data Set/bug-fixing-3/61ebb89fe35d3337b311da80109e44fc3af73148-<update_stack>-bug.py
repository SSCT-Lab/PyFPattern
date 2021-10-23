def update_stack(module, stack_params, cfn):
    if (('TemplateBody' not in stack_params) and ('TemplateURL' not in stack_params)):
        stack_params['UsePreviousTemplate'] = True
    try:
        cfn.update_stack(**stack_params)
        result = stack_operation(cfn, stack_params['StackName'], 'UPDATE')
    except Exception as err:
        error_msg = boto_exception(err)
        if ('No updates are to be performed.' in error_msg):
            result = dict(changed=False, output='Stack is already up-to-date.')
        else:
            module.fail_json(msg=error_msg)
    if (not result):
        module.fail_json(msg='empty result')
    return result