

def load_config(module, commands):
    (rc, out, err) = exec_command(module, 'config')
    if (rc != 0):
        module.fail_json(msg='unable to enter configuration mode', err=to_text(out, errors='surrogate_then_replace'))
    for command in to_list(commands):
        if (command == 'end'):
            continue
        (rc, out, err) = exec_command(module, command)
        if (rc != 0):
            module.fail_json(msg=to_text(err, errors='surrogate_then_replace'), command=command, rc=rc)
    exec_command(module, 'end')
