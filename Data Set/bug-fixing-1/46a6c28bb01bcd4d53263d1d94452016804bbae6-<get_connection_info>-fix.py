

def get_connection_info(module):
    url = module.params.get('api_url')
    username = module.params.get('api_username')
    password = module.params.get('api_password')
    if (not url):
        url = os.environ.get('ONE_URL')
    if (not username):
        username = os.environ.get('ONE_USERNAME')
    if (not password):
        password = os.environ.get('ONE_PASSWORD')
    if (not username):
        if (not password):
            authfile = os.environ.get('ONE_AUTH')
            if (authfile is None):
                authfile = os.path.join(os.environ.get('HOME'), '.one', 'one_auth')
            try:
                authstring = open(authfile, 'r').read().rstrip()
                username = authstring.split(':')[0]
                password = authstring.split(':')[1]
            except (OSError, IOError):
                module.fail_json(msg=("Could not find or read ONE_AUTH file at '%s'" % authfile))
            except Exception:
                module.fail_json(msg=("Error occurs when read ONE_AUTH file at '%s'" % authfile))
    if (not url):
        module.fail_json(msg='Opennebula API url (api_url) is not specified')
    from collections import namedtuple
    auth_params = namedtuple('auth', ('url', 'username', 'password'))
    return auth_params(url=url, username=username, password=password)
