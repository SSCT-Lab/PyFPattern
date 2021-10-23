def edit_config_or_macro(connection, commands):
    if ('macro name' in commands[0]):
        connection.edit_macro(candidate=commands)
    else:
        connection.edit_config(candidate=commands)