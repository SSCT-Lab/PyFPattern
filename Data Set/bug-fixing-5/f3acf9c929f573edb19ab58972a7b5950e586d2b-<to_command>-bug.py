def to_command(module, commands):
    if is_nxapi(module):
        default_output = 'json'
    else:
        default_output = 'text'
    transform = ComplexList(dict(command=dict(key=True), output=dict(default=default_output), prompt=dict(), answer=dict()), module)
    commands = transform(to_list(commands))
    for (index, item) in enumerate(commands):
        if is_json(item['command']):
            item['output'] = 'json'
        elif is_text(item['command']):
            item['output'] = 'text'
    return commands