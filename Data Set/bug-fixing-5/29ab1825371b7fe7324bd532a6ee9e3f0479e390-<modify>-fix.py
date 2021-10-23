def modify(module, conn, name, values):
    ' Modify ElastiCache parameter group to reflect the new information if it differs from the current. '
    format_parameters = []
    for key in values:
        value = to_text(values[key])
        format_parameters.append({
            'ParameterName': key,
            'ParameterValue': value,
        })
    try:
        response = conn.modify_cache_parameter_group(CacheParameterGroupName=name, ParameterNameValues=format_parameters)
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg='Unable to modify cache parameter group.', exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
    return response