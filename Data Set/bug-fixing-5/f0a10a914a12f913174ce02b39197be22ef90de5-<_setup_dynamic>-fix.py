def _setup_dynamic(self):
    'Create a CloudStack simulator using docker.'
    config = self._read_config_template()
    self.container_name = self.DOCKER_SIMULATOR_NAME
    results = docker_inspect(self.args, self.container_name)
    if (results and (not results[0]['State']['Running'])):
        docker_rm(self.args, self.container_name)
        results = []
    if results:
        display.info('Using the existing CloudStack simulator docker container.', verbosity=1)
    else:
        display.info('Starting a new CloudStack simulator docker container.', verbosity=1)
        docker_pull(self.args, self.image)
        docker_run(self.args, self.image, ['-d', '-p', '8888:8888', '--name', self.container_name])
        docker_exec(self.args, self.container_name, ['find', '/var/lib/mysql', '-type', 'f', '-exec', 'touch', '{}', ';'])
        if (not self.args.explain):
            display.notice('The CloudStack simulator will probably be ready in 5 - 10 minutes.')
    container_id = get_docker_container_id()
    if container_id:
        display.info(('Running in docker container: %s' % container_id), verbosity=1)
        self.host = self._get_simulator_address()
        display.info(('Found CloudStack simulator container address: %s' % self.host), verbosity=1)
    else:
        self.host = 'localhost'
    self.port = 8888
    self.endpoint = ('http://%s:%d' % (self.host, self.port))
    self._wait_for_service()
    if self.args.explain:
        values = dict(HOST=self.host, PORT=str(self.port))
    else:
        credentials = self._get_credentials()
        if self.args.docker:
            host = self.DOCKER_SIMULATOR_NAME
        else:
            host = self.host
        values = dict(HOST=host, PORT=str(self.port), KEY=credentials['apikey'], SECRET=credentials['secretkey'])
    config = self._populate_config_template(config, values)
    self._write_config(config)