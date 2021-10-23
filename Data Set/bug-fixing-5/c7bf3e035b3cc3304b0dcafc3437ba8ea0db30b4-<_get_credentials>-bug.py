def _get_credentials(self, params):
    self.log('Getting credentials')
    arg_credentials = dict()
    for (attribute, env_variable) in AZURE_CREDENTIAL_ENV_MAPPING.items():
        arg_credentials[attribute] = params.get(attribute, None)
    auth_source = params.get('auth_source', None)
    if (not auth_source):
        auth_source = os.environ.get('ANSIBLE_AZURE_AUTH_SOURCE', 'auto')
    if (auth_source == 'msi'):
        self.log('Retrieving credenitals from MSI')
        return self._get_msi_credentials(arg_credentials['subscription_id'], client_id=params.get('client_id', None))
    if (auth_source == 'cli'):
        if (not HAS_AZURE_CLI_CORE):
            self.fail(msg=missing_required_lib('azure-cli', reason='for `cli` auth_source'), exception=HAS_AZURE_CLI_CORE_EXC)
        try:
            self.log('Retrieving credentials from Azure CLI profile')
            cli_credentials = self._get_azure_cli_credentials()
            return cli_credentials
        except CLIError as err:
            self.fail('Azure CLI profile cannot be loaded - {0}'.format(err))
    if (auth_source == 'env'):
        self.log('Retrieving credentials from environment')
        env_credentials = self._get_env_credentials()
        return env_credentials
    if (auth_source == 'credential_file'):
        self.log('Retrieving credentials from credential file')
        profile = params.get('profile', 'default')
        default_credentials = self._get_profile(profile)
        return default_credentials
    if (arg_credentials['profile'] is not None):
        self.log('Retrieving credentials with profile parameter.')
        credentials = self._get_profile(arg_credentials['profile'])
        return credentials
    if arg_credentials['subscription_id']:
        self.log('Received credentials from parameters.')
        return arg_credentials
    env_credentials = self._get_env_credentials()
    if env_credentials:
        self.log('Received credentials from env.')
        return env_credentials
    default_credentials = self._get_profile()
    if default_credentials:
        self.log('Retrieved default profile credentials from ~/.azure/credentials.')
        return default_credentials
    try:
        if HAS_AZURE_CLI_CORE:
            self.log('Retrieving credentials from AzureCLI profile')
        cli_credentials = self._get_azure_cli_credentials()
        return cli_credentials
    except CLIError as ce:
        self.log('Error getting AzureCLI profile credentials - {0}'.format(ce))
    return None