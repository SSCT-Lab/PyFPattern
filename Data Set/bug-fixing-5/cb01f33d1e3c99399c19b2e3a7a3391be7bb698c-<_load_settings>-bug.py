def _load_settings(self):
    basename = os.path.splitext(os.path.basename(__file__))[0]
    default_path = os.path.join(os.path.dirname(__file__), (basename + '.ini'))
    path = os.path.expanduser(os.path.expandvars(os.environ.get('AZURE_INI_PATH', default_path)))
    config = None
    settings = None
    try:
        config = ConfigParser.ConfigParser()
        config.read(path)
    except:
        pass
    if (config is not None):
        settings = dict()
        for key in AZURE_CONFIG_SETTINGS:
            try:
                settings[key] = config.get('azure', key, raw=True)
            except:
                pass
    return settings