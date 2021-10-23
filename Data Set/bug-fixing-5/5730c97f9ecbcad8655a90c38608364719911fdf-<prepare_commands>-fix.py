def prepare_commands(commands):
    ' transforms a list of Command objects to dict\n\n    :param commands: list of Command objects\n\n    :returns: list of dict objects\n    '
    jsonify = (lambda x: ('%s | json' % x))
    for item in to_list(commands):
        if (item.output == 'json'):
            cmd = jsonify(cmd)
        elif item.command.endswith('| json'):
            item.output = 'json'
            cmd = str(item)
        else:
            cmd = str(item)
        (yield cmd)