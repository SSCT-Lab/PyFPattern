

def run(self):
    super(GalaxyCLI, self).run()
    self.galaxy = Galaxy()

    def server_config_def(section, key, required):
        return {
            'description': ('The %s of the %s Galaxy server' % (key, section)),
            'ini': [{
                'section': ('galaxy_server.%s' % section),
                'key': key,
            }],
            'env': [{
                'name': ('ANSIBLE_GALAXY_SERVER_%s_%s' % (section.upper(), key.upper())),
            }],
            'required': required,
        }
    server_def = [('url', True), ('username', False), ('password', False), ('token', False)]
    config_servers = []
    for server_key in (C.GALAXY_SERVER_LIST or []):
        config_dict = dict(((k, server_config_def(server_key, k, req)) for (k, req) in server_def))
        defs = AnsibleLoader(yaml.safe_dump(config_dict)).get_single_data()
        C.config.initialize_plugin_configuration_definitions('galaxy_server', server_key, defs)
        server_options = C.config.get_plugin_options('galaxy_server', server_key)
        token_val = (server_options['token'] or NoTokenSentinel)
        server_options['token'] = GalaxyToken(token=token_val)
        config_servers.append(GalaxyAPI(self.galaxy, server_key, **server_options))
    cmd_server = context.CLIARGS['api_server']
    cmd_token = GalaxyToken(token=context.CLIARGS['api_key'])
    if cmd_server:
        config_server = next((s for s in config_servers if (s.name == cmd_server)), None)
        if config_server:
            self.api_servers.append(config_server)
        else:
            self.api_servers.append(GalaxyAPI(self.galaxy, 'cmd_arg', cmd_server, token=cmd_token))
    else:
        self.api_servers = config_servers
    if (len(self.api_servers) == 0):
        self.api_servers.append(GalaxyAPI(self.galaxy, 'default', C.GALAXY_SERVER, token=cmd_token))
    context.CLIARGS['func']()
