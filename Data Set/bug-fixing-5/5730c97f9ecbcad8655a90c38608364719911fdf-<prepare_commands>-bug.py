def prepare_commands(commands):
    ' transforms a list of Command objects to dict\n\n    :param commands: list of Command objects\n\n    :returns: list of dict objects\n    '
    jsonify = (lambda x: ('%s | json' % x))
    for cmd in to_list(commands):
        if (cmd.output == 'json'):
            cmd = jsonify(cmd)
        else:
            cmd = str(cmd)
        (yield cmd)