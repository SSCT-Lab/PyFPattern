def verify_file(self, path):
    '\n        Verify plugin configuration file and mark this plugin active\n        Args:\n            path: Path of configuration YAML file\n\n        Returns: True if everything is correct, else False\n\n        '
    valid = False
    if super(InventoryModule, self).verify_file(path):
        if path.endswith(('vmware.yaml', 'vmware.yml')):
            valid = True
    if (not HAS_REQUESTS):
        raise AnsibleParserError('Please install "requests" Python module as this is required for VMware Guest dynamic inventory plugin.')
    elif (not HAS_PYVMOMI):
        raise AnsibleParserError('Please install "PyVmomi" Python module as this is required for VMware Guest dynamic inventory plugin.')
    if HAS_REQUESTS:
        required_version = (2, 3)
        requests_version = requests.__version__.split('.')[:2]
        try:
            requests_major_minor = tuple(map(int, requests_version))
        except ValueError:
            raise AnsibleParserError("Failed to parse 'requests' library version.")
        if (requests_major_minor < required_version):
            raise AnsibleParserError(("'requests' library version should be >= %s, found: %s." % ('.'.join([str(w) for w in required_version]), requests.__version__)))
        valid = True
    return valid