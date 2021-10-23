def check_valid_modification(module, values, modifiable_params):
    ' Check if the parameters and values in values are valid.  '
    changed_with_update = False
    for parameter in values:
        new_value = values[parameter]
        if (parameter not in modifiable_params):
            module.fail_json(msg=('%s is not a modifiable parameter. Valid parameters to modify are: %s.' % (parameter, modifiable_params.keys())))
        str_to_type = {
            'integer': int,
            'string': string_types,
        }
        expected_type = str_to_type[modifiable_params[parameter][1]]
        if (not isinstance(new_value, expected_type)):
            if (expected_type == str):
                if isinstance(new_value, bool):
                    values[parameter] = ('yes' if new_value else 'no')
                else:
                    values[parameter] = to_text(new_value)
            elif (expected_type == int):
                if isinstance(new_value, bool):
                    values[parameter] = (1 if new_value else 0)
                else:
                    module.fail_json(msg=('%s (type %s) is not an allowed value for the parameter %s. Expected a type %s.' % (new_value, type(new_value), parameter, modifiable_params[parameter][1])))
            else:
                module.fail_json(msg=('%s (type %s) is not an allowed value for the parameter %s. Expected a type %s.' % (new_value, type(new_value), parameter, modifiable_params[parameter][1])))
        choices = modifiable_params[parameter][0]
        if choices:
            if (not ((to_text(new_value) in choices) or isinstance(new_value, int))):
                module.fail_json(msg=('%s is not an allowed value for the parameter %s. Valid parameters are: %s.' % (new_value, parameter, choices)))
        if (to_text(values[parameter]) != modifiable_params[parameter][2]):
            changed_with_update = True
    return (changed_with_update, values)