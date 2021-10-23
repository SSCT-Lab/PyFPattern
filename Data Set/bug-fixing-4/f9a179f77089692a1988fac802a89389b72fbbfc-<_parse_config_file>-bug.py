def _parse_config_file(self):
    config = dict()
    config_path = None
    if self._args.config_file:
        config_path = self._args.config_file
    elif self._env_args.config_file:
        config_path = self._env_args.config_file
    if config_path:
        try:
            config_file = os.path.abspath(config_path)
        except:
            config_file = None
        if (config_file and os.path.exists(config_file)):
            with open(config_file) as f:
                try:
                    config = yaml.safe_load(f.read())
                except Exception as exc:
                    self.fail(('Error: parsing %s - %s' % (config_path, str(exc))))
    return config