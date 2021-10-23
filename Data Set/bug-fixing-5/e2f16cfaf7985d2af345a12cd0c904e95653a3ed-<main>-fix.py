def main():
    config = ConfigManager()
    username = (get_ini_config_value(config._parser, dict(section='vault', key='username')) or getpass.getuser())
    keyname = (get_ini_config_value(config._parser, dict(section='vault', key='keyname')) or 'ansible')
    if ((len(sys.argv) == 2) and (sys.argv[1] == 'set')):
        intro = 'Storing password in "{}" user keyring using key name: {}\n'
        sys.stdout.write(intro.format(username, keyname))
        password = getpass.getpass()
        confirm = getpass.getpass('Confirm password: ')
        if (password == confirm):
            keyring.set_password(keyname, username, password)
        else:
            sys.stderr.write('Passwords do not match\n')
            sys.exit(1)
    else:
        sys.stdout.write('{}\n'.format(keyring.get_password(keyname, username)))
    sys.exit(0)