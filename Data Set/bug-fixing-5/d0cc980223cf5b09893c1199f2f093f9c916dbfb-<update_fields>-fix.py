def update_fields(p):
    'This updates the module field names\n    to match the field names tower-cli expects to make\n    calling of the modify/delete methods easier.\n    '
    params = p.copy()
    field_map = {
        'ask_extra_vars': 'ask_variables_on_launch',
        'ask_limit': 'ask_limit_on_launch',
        'ask_tags': 'ask_tags_on_launch',
        'ask_job_type': 'ask_job_type_on_launch',
        'machine_credential': 'credential',
    }
    params_update = {
        
    }
    for (old_k, new_k) in field_map.items():
        v = params.pop(old_k)
        params_update[new_k] = v
    extra_vars = params.get('extra_vars_path')
    if (extra_vars is not None):
        params_update['extra_vars'] = [('@' + extra_vars)]
    params.update(params_update)
    return params