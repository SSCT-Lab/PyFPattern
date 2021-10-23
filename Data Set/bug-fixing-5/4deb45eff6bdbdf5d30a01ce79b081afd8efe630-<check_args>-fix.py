def check_args(module, warnings):
    iosxr_check_args(module, warnings)
    if module.params['comment']:
        if (len(module.params['comment']) > 60):
            module.fail_json(msg='comment argument cannot be more than 60 characters')
    if module.params['force']:
        warnings.append('The force argument is deprecated, please use match=none instead.  This argument will be removed in the future')