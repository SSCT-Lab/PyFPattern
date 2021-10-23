

def map_config_to_obj(module):
    templatized_command = '%(ovs-vsctl)s -t %(timeout)s list %(table)s %(record)s'
    command = (templatized_command % module.params)
    (rc, out, err) = module.run_command(command, check_rc=True)
    if (rc != 0):
        module.fail_json(msg=err)
    match = re.search((('^' + module.params['col']) + '(\\s+):(\\s+)(.*)$'), out, re.M)
    col_value = match.group(3)
    col_value_to_dict = {
        
    }
    if (col_value and (col_value != '{}')):
        for kv in col_value[1:(- 1)].split(','):
            (k, v) = kv.split('=')
            col_value_to_dict[k.strip()] = v.strip()
    obj = {
        'table': module.params['table'],
        'record': module.params['record'],
        'col': module.params['col'],
    }
    if (module.params['key'] in col_value_to_dict):
        obj['key'] = module.params['key']
        obj['value'] = col_value_to_dict[module.params['key']]
    return obj
