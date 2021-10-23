def check_client_version(self, client_name, client_version, expected_version):
    if (Version(client_version) < Version(expected_version)):
        self.fail('Installed {0} client version is {1}. The supported version is {2}. Try `pip install azure>={3} --upgrade`'.format(client_name, client_version, expected_version, AZURE_MIN_RELEASE))