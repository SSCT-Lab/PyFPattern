

def edit_config_or_macro(connection, commands):
    if commands[0].startswith('macro name'):
        connection.edit_macro(candidate=commands)
    else:
        connection.edit_config(candidate=commands)
