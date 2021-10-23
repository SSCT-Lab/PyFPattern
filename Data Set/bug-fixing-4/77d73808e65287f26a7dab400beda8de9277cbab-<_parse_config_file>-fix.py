def _parse_config_file(self):
    config = dict()
    config_file = DEFAULT_DOCKER_CONFIG_FILE
    if self._args.config_file:
        config_file = self._args.config_file
    elif self._env_args.config_file:
        config_file = self._env_args.config_file
    config_file = os.path.abspath(config_file)
    if os.path.isfile(config_file):
        with open(config_file) as f:
            try:
                config = yaml.safe_load(f.read())
            except Exception as exc:
                self.fail(('Error: parsing %s - %s' % (config_file, str(exc))))
    else:
        msg = ('Error: config file given by {} does not exist - ' + config_file)
        if self._args.config_file:
            self.fail(msg.format('command line argument'))
        elif self._env_args.config_file:
            self.fail(msg.format(DOCKER_ENV_ARGS.get('config_file')))
        else:
            self.log(msg.format('DEFAULT_DOCKER_CONFIG_FILE'))
    return config