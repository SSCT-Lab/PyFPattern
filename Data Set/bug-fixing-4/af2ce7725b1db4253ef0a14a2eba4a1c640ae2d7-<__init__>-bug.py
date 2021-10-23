def __init__(self, galaxy, name, src=None, version=None, scm=None, path=None):
    self._metadata = None
    self._install_info = None
    self._validate_certs = (not galaxy.options.ignore_certs)
    display.debug(('Validate TLS certificates: %s' % self._validate_certs))
    self.options = galaxy.options
    self.galaxy = galaxy
    self.name = name
    self.version = version
    self.src = (src or name)
    self.scm = scm
    if (path is not None):
        if (self.name not in path):
            path = os.path.join(path, self.name)
        self.path = path
    else:
        for role_path_dir in galaxy.roles_paths:
            role_path = os.path.join(role_path_dir, self.name)
            if os.path.exists(role_path):
                self.path = role_path
                break
        else:
            self.path = os.path.join(galaxy.roles_paths[0], self.name)