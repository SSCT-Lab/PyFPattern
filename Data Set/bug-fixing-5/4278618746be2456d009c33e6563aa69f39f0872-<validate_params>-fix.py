def validate_params(module, aws):
    '\n    Performs basic parameter validation.\n\n    :param module:\n    :param aws:\n    :return:\n    '
    function_name = module.params['lambda_function_arn']
    if (not re.search('^[\\w\\-:]+$', function_name)):
        module.fail_json(msg='Function name {0} is invalid. Names must contain only alphanumeric characters and hyphens.'.format(function_name))
    if ((len(function_name) > 64) and (not function_name.startswith('arn:aws:lambda:'))):
        module.fail_json(msg='Function name "{0}" exceeds 64 character limit'.format(function_name))
    elif ((len(function_name) > 140) and function_name.startswith('arn:aws:lambda:')):
        module.fail_json(msg='ARN "{0}" exceeds 140 character limit'.format(function_name))
    if (not module.params['lambda_function_arn'].startswith('arn:aws:lambda:')):
        function_name = module.params['lambda_function_arn']
        module.params['lambda_function_arn'] = 'arn:aws:lambda:{0}:{1}:function:{2}'.format(aws.region, aws.account_id, function_name)
    qualifier = get_qualifier(module)
    if qualifier:
        function_arn = module.params['lambda_function_arn']
        module.params['lambda_function_arn'] = '{0}:{1}'.format(function_arn, qualifier)
    return