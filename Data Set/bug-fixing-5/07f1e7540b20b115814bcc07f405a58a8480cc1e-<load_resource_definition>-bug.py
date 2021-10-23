def load_resource_definition(self, src):
    ' Load the requested src path '
    result = None
    path = os.path.normpath(src)
    self.helper.log('Reading definition from {}'.format(path))
    if (not os.path.exists(path)):
        self.fail_json(msg='Error accessing {}. Does the file exist?'.format(path))
    try:
        result = yaml.safe_load(open(path, 'r'))
    except (IOError, yaml.YAMLError) as exc:
        self.fail_json(msg='Error loading resource_definition: {}'.format(exc))
    return result