

def _load_config(module, config):
    'Sends configuration commands to the remote device\n    '
    (rc, out, err) = exec_command(module, 'mmi-mode enable')
    if (rc != 0):
        module.fail_json(msg='unable to set mmi-mode enable', output=err)
    (rc, out, err) = exec_command(module, 'system-view immediately')
    if (rc != 0):
        module.fail_json(msg='unable to enter system-view', output=err)
    for (index, cmd) in enumerate(config):
        (rc, out, err) = exec_command(module, cmd)
        if (rc != 0):
            print_msg = cli_err_msg(cmd.strip(), err)
            exec_command(module, 'quit')
            (rc, out, err) = exec_command(module, cmd)
            if (rc != 0):
                print_msg1 = cli_err_msg(cmd.strip(), err)
                if (not re.findall('unrecognized command found', print_msg1)):
                    print_msg = print_msg1
                exec_command(module, 'return')
                exec_command(module, 'system-view immediately')
                (rc, out, err) = exec_command(module, cmd)
                if (rc != 0):
                    print_msg2 = cli_err_msg(cmd.strip(), err)
                    if (not re.findall('unrecognized command found', print_msg2)):
                        print_msg = print_msg2
                    module.fail_json(msg=print_msg)
    (rc, out, err) = exec_command(module, 'return')
    if (rc != 0):
        module.fail_json(msg='unable to return', output=err)
    (rc, out, err) = exec_command(module, 'undo mmi-mode enable')
    if (rc != 0):
        module.fail_json(msg='unable to undo mmi-mode enable', output=err)
