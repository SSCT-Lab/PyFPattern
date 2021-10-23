

def to_command(module, commands):
    if is_nxapi(module):
        default_output = 'json'
    else:
        default_output = 'text'
    transform = ComplexList(dict(command=dict(key=True), output=dict(default=default_output), prompt=dict(), answer=dict()), module)
    commands = transform(to_list(commands))
    for item in commands:
        if is_json(item['command']):
            item['output'] = 'json'
    return commands
