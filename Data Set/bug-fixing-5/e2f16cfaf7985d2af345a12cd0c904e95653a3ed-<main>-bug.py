def main():
    (parser, config_path) = C.load_config_file()
    if parser.has_option('vault', 'username'):
        username = parser.get('vault', 'username')
    else:
        username = getpass.getuser()
    if parser.has_option('vault', 'keyname'):
        keyname = parser.get('vault', 'keyname')
    else:
        keyname = 'ansible'
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