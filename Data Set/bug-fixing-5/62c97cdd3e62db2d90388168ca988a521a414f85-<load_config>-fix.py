def load_config(module, commands):
    conn = connection(module)
    (rc, out, err) = conn.exec_command('configure terminal')
    if (rc != 0):
        module.fail_json(msg='unable to enter configuration mode', err=err)
    for command in to_list(commands):
        if (command == 'end'):
            continue
        (rc, out, err) = conn.exec_command(command)
        if (rc != 0):
            module.fail_json(msg=err, command=command, rc=rc)
    conn.exec_command('end')