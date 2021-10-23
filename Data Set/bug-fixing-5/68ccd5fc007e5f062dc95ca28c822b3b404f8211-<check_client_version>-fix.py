def check_client_version(self, client_type):
    package_version = AZURE_PKG_VERSIONS.get(client_type.__name__, None)
    if (package_version is not None):
        client_name = package_version.get('package_name')
        client_version = package_version.get('installed_version')
        expected_version = package_version.get('expected_version')
        if (Version(client_version) < Version(expected_version)):
            self.fail('Installed {0} client version is {1}. The supported version is {2}. Try `pip install ansible[azure]`'.format(client_name, client_version, expected_version, AZURE_MIN_RELEASE))