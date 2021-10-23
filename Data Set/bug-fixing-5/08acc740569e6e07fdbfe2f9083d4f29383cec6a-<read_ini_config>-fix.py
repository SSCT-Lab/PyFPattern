def read_ini_config(self):
    ini_group = self.module.params.get('api_account')
    paths = (os.path.join(os.path.expanduser('~'), '.vultr.ini'), os.path.join(os.getcwd(), 'vultr.ini'))
    if ('VULTR_API_CONFIG' in os.environ):
        paths += (os.path.expanduser(os.environ['VULTR_API_CONFIG']),)
    conf = configparser.ConfigParser()
    conf.read(paths)
    if (not conf._sections.get(ini_group)):
        return dict()
    return dict(conf.items(ini_group))