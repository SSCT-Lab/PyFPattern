def _configure_from_file(self):
    "Initialize from .ini file.\n\n        Configuration file is assumed to be named 'brook.ini' and to be located on the same\n        directory than this file, unless the environment variable BROOK_INI_PATH says otherwise.\n        "
    brook_ini_default_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'brook.ini')
    brook_ini_path = os.environ.get('BROOK_INI_PATH', brook_ini_default_path)
    config = ConfigParser(defaults={
        'api_token': '',
        'project_id': '',
    })
    config.read(brook_ini_path)
    self.api_token = config.get('brook', 'api_token')
    self.project_id = config.get('brook', 'project_id')
    if (not self.api_token):
        print('You must provide (at least) your Brook.io API token to generate the dynamic inventory.')
        sys.exit(1)