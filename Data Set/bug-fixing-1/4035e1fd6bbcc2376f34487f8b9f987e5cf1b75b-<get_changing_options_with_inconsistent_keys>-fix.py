

def get_changing_options_with_inconsistent_keys(modify_params, instance, purge_cloudwatch_logs):
    changing_params = {
        
    }
    current_options = get_current_attributes_with_inconsistent_keys(instance)
    for option in current_options:
        current_option = current_options[option]
        desired_option = modify_params.pop(option, None)
        if (desired_option is None):
            continue
        if isinstance(current_option, list):
            if isinstance(desired_option, list):
                if (set(desired_option) <= set(current_option)):
                    continue
            elif isinstance(desired_option, string_types):
                if (desired_option in current_option):
                    continue
        if (current_option == desired_option):
            continue
        if ((option == 'ProcessorFeatures') and (desired_option == [])):
            changing_params['UseDefaultProcessorFeatures'] = True
        elif (option == 'CloudwatchLogsExportConfiguration'):
            current_option = set(current_option.get('LogTypesToEnable', []))
            desired_option = set(desired_option)
            format_option = {
                'EnableLogTypes': [],
                'DisableLogTypes': [],
            }
            format_option['EnableLogTypes'] = list(desired_option.difference(current_option))
            if purge_cloudwatch_logs:
                format_option['DisableLogTypes'] = list(current_option.difference(desired_option))
            if (format_option['EnableLogTypes'] or format_option['DisableLogTypes']):
                changing_params[option] = format_option
        else:
            changing_params[option] = desired_option
    return changing_params
