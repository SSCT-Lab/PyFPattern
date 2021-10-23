def get_config(module, flags):
    'Retrieves the current config from the device or cache'
    flags = ([] if (flags is None) else flags)
    cmd = 'display current-configuration '
    cmd += ' '.join(flags)
    cmd = cmd.strip()
    (rc, out, err) = exec_command(module, cmd)
    if (rc != 0):
        module.fail_json(msg=err)
    config = str(out).strip()
    if config.startswith('display'):
        configs = config.split('\n')
        if (len(configs) > 1):
            return '\n'.join(configs[1:])
        else:
            return ''
    else:
        return config