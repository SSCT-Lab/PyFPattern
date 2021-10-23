def load_config(module, config, commit=False):
    exec_command(module, 'configure')
    for item in to_list(config):
        (rc, out, err) = exec_command(module, item)
        if (rc != 0):
            module.fail_json(msg=str(err))
    exec_command(module, 'top')
    (rc, diff, err) = exec_command(module, 'show | compare')
    if commit:
        exec_command(module, 'commit and-quit')
    else:
        for cmd in ['rollback 0', 'exit']:
            exec_command(module, cmd)
    return str(diff).strip()