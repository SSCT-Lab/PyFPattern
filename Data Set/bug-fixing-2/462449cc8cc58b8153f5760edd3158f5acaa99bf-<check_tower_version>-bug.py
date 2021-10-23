

def check_tower_version(self, fallback=None):
    'Check the Tower version being tested and determine the correct CLI version to use.\n        :type fallback: str | None\n        '
    tower_cli_version_map = {
        '3.1.5': '3.1.8',
        '3.2.3': '3.2.1',
    }
    cli_version = tower_cli_version_map.get(self.version, fallback)
    if (not cli_version):
        raise ApplicationError(('Mapping to ansible-tower-cli version required for Tower version: %s' % self.version))
    self._set_cloud_config('tower_cli_version', cli_version)
