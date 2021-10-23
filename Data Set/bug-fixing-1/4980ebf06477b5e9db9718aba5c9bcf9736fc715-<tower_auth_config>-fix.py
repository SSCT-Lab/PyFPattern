

def tower_auth_config(module):
    'tower_auth_config attempts to load the tower-cli.cfg file\n    specified from the `tower_config_file` parameter. If found,\n    if returns the contents of the file as a dictionary, else\n    it will attempt to fetch values from the module pararms and\n    only pass those values that have been set.\n    '
    config_file = module.params.get('tower_config_file')
    if config_file:
        config_file = os.path.expanduser(config_file)
        if (not os.path.exists(config_file)):
            module.fail_json(msg=('file not found: %s' % config_file))
        if os.path.isdir(config_file):
            module.fail_json(msg=('directory can not be used as config file: %s' % config_file))
        with open(config_file, 'rb') as f:
            return parser.string_to_dict(f.read())
    else:
        auth_config = {
            
        }
        host = module.params.get('tower_host')
        if host:
            auth_config['host'] = host
        username = module.params.get('tower_username')
        if username:
            auth_config['username'] = username
        password = module.params.get('tower_password')
        if password:
            auth_config['password'] = password
        verify_ssl = module.params.get('tower_verify_ssl')
        if (verify_ssl is not None):
            auth_config['verify_ssl'] = verify_ssl
        return auth_config
