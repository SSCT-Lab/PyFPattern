

def append_param(rule, param, flag, is_list):
    if is_list:
        for item in param:
            append_param(rule, item, flag, False)
    elif (param is not None):
        rule.extend([flag, param])
