def create_connection():
    '\n    Create a connection to oVirt engine API.\n    '
    default_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ovirt.ini')
    config_path = os.environ.get('OVIRT_INI_PATH', default_path)
    config = ConfigParser.SafeConfigParser(defaults={
        'ovirt_url': None,
        'ovirt_username': None,
        'ovirt_password': None,
        'ovirt_ca_file': None,
    })
    if (not config.has_section('ovirt')):
        config.add_section('ovirt')
    config.read(config_path)
    return sdk.Connection(url=config.get('ovirt', 'ovirt_url'), username=config.get('ovirt', 'ovirt_username'), password=config.get('ovirt', 'ovirt_password'), ca_file=config.get('ovirt', 'ovirt_ca_file', None), insecure=(config.get('ovirt', 'ovirt_ca_file', None) is None))