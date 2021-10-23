def map_config_to_obj(module):
    cmd = 'show configuration system services netconf'
    (rc, out, err) = exec_command(module, cmd)
    if (rc != 0):
        module.fail_json(msg='unable to retrieve current config', stderr=err)
    config = str(out).strip()
    obj = {
        'state': 'absent',
    }
    if ('ssh' in config):
        obj.update({
            'state': 'present',
            'netconf_port': parse_port(config),
        })
    return obj