def map_obj_to_commands(updates, module):
    commands = list()
    state = module.params['state']
    update_password = module.params['update_password']
    password_type = module.params['password_type']

    def needs_update(want, have, x):
        return (want.get(x) and (want.get(x) != have.get(x)))

    def add(command, want, x):
        command.append(('username %s %s' % (want['name'], x)))

    def add_hashed_password(command, want, x):
        command.append(('username %s secret %s %s' % (want['name'], ast.literal_eval(x)['type'], ast.literal_eval(x)['value'])))

    def add_ssh(command, want, x=None):
        command.append('ip ssh pubkey-chain')
        if x:
            command.append(('username %s' % want['name']))
            command.append(('key-hash %s' % x))
            command.append('exit')
        else:
            command.append(('no username %s' % want['name']))
        command.append('exit')
    for update in updates:
        (want, have) = update
        if (want['state'] == 'absent'):
            if have['sshkey']:
                add_ssh(commands, want)
            else:
                commands.append(user_del_cmd(want['name']))
        if needs_update(want, have, 'view'):
            add(commands, want, ('view %s' % want['view']))
        if needs_update(want, have, 'privilege'):
            add(commands, want, ('privilege %s' % want['privilege']))
        if needs_update(want, have, 'sshkey'):
            add_ssh(commands, want, want['sshkey'])
        if needs_update(want, have, 'configured_password'):
            if ((update_password == 'always') or (not have)):
                if (have and (password_type != have['password_type'])):
                    module.fail_json(msg=('Can not have both a user password and a user secret.' + ' Please choose one or the other.'))
                add(commands, want, ('%s %s' % (password_type, want['configured_password'])))
        if needs_update(want, have, 'hashed_password'):
            add_hashed_password(commands, want, want['hashed_password'])
        if needs_update(want, have, 'nopassword'):
            if want['nopassword']:
                add(commands, want, 'nopassword')
            else:
                add(commands, want, user_del_cmd(want['name']))
    return commands