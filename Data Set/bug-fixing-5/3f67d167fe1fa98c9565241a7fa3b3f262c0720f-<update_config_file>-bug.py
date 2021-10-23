def update_config_file(self):
    '\n        If the authorization not stored in the config file or reauthorize is True,\n        update the config file with the new authorization.\n\n        :return: None\n        '
    path = os.path.expanduser(self.config_path)
    if (not self.config_file_exists(path)):
        self.create_config_file(path)
    try:
        config = json.load(open(path, 'r'))
    except ValueError:
        self.log(('Error reading config from %s' % path))
        config = dict()
    if (not config.get('auths')):
        self.log('Adding auths dict to config.')
        config['auths'] = dict()
    if (not config['auths'].get(self.registry_url)):
        self.log(('Adding registry_url %s to auths.' % self.registry_url))
        config['auths'][self.registry_url] = dict()
    encoded_credentials = dict(auth=base64.b64encode(((self.username + b':') + self.password)), email=self.email)
    if ((config['auths'][self.registry_url] != encoded_credentials) or self.reauthorize):
        config['auths'][self.registry_url] = encoded_credentials
        self.log(('Updating config file %s with new authorization for %s' % (path, self.registry_url)))
        self.results['actions'].append(('Updated config file %s with new authorization for %s' % (path, self.registry_url)))
        self.results['changed'] = True
        self.write_config(path, config)