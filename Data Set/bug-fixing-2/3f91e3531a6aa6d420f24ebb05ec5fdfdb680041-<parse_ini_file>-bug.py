

def parse_ini_file(self):
    config = configparser.SafeConfigParser()
    config.read((os.path.dirname(os.path.realpath(__file__)) + '/nagios_livestatus.ini'))
    for section in config.sections():
        if (not config.has_option(section, 'livestatus_uri')):
            continue
        fields_to_retrieve = self.default_fields_to_retrieve
        if config.has_option(section, 'fields_to_retrieve'):
            fields_to_retrieve = [field.strip() for field in config.get(section, 'fields_to_retrieve').split(',')]
            fields_to_retrieve = tuple(fields_to_retrieve)
        section_values = {
            'var_prefix': 'livestatus_',
            'host_filter': None,
            'host_field': 'name',
            'group_field': 'groups',
        }
        for (key, value) in section_values.iteritems():
            if config.has_option(section, key):
                section_values[key] = config.get(section, key).strip()
        livestatus_uri = config.get(section, 'livestatus_uri')
        backend_definition = None
        unix_match = re.match('unix:(.*)', livestatus_uri)
        if (unix_match is not None):
            backend_definition = {
                'connection': unix_match.group(1),
            }
        tcp_match = re.match('tcp:(.*):([^:]*)', livestatus_uri)
        if (tcp_match is not None):
            backend_definition = {
                'connection': (tcp_match.group(1), int(tcp_match.group(2))),
            }
        if (backend_definition is None):
            raise Exception(('livestatus_uri field is invalid (%s). Expected: unix:/path/to/live or tcp:host:port' % livestatus_uri))
        backend_definition['name'] = section
        backend_definition['fields'] = fields_to_retrieve
        for (key, value) in section_values.iteritems():
            backend_definition[key] = value
        self.backends.append(backend_definition)
