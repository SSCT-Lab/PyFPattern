def read_ini_config(self):
    ini_group = self.module.params.get('api_account')
    keys = ['key', 'timeout', 'retries', 'endpoint']
    env_conf = {
        
    }
    for key in keys:
        if (('VULTR_API_%s' % key.upper()) not in os.environ):
            break
        else:
            env_conf[key] = os.environ[('VULTR_API_%s' % key.upper())]
    else:
        return env_conf
    paths = (os.path.join(os.path.expanduser('~'), '.vultr.ini'), os.path.join(os.getcwd(), 'vultr.ini'))
    if ('VULTR_API_CONFIG' in os.environ):
        paths += (os.path.expanduser(os.environ['VULTR_API_CONFIG']),)
    if (not any((os.path.exists(c) for c in paths))):
        self.module.fail_json(msg=('Config file not found. Tried : %s' % ', '.join(paths)))
    conf = configparser.ConfigParser()
    conf.read(paths)
    return dict(conf.items(ini_group))