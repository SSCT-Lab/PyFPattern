def prepare_commands(commands):
    jsonify = (lambda x: ('%s | json' % x))
    for cmd in to_list(commands):
        if (cmd.output == 'json'):
            cmd.command_string = jsonify(cmd)
        (yield cmd)