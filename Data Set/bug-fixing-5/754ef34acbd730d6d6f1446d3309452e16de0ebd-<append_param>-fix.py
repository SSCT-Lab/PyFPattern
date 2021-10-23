def append_param(rule, param, flag, is_list):
    if is_list:
        for item in param:
            append_param(rule, item, flag, False)
    elif (param is not None):
        if (param[0] == '!'):
            rule.extend(['!', flag, param[1:]])
        else:
            rule.extend([flag, param])