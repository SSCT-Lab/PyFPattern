def _get_credentials(self, params):
    self.log('Getting credentials')
    arg_credentials = dict()
    for (attribute, env_variable) in AZURE_CREDENTIAL_ENV_MAPPING.items():
        arg_credentials[attribute] = getattr(params, attribute)
    if (arg_credentials['profile'] is not None):
        self.log('Retrieving credentials with profile parameter.')
        credentials = self._get_profile(arg_credentials['profile'])
        return credentials
    if (arg_credentials['client_id'] is not None):
        self.log('Received credentials from parameters.')
        return arg_credentials
    if (arg_credentials['ad_user'] is not None):
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
    msi_credentials = self._get_msi_credentials(arg_credentials.get('subscription_id'))
    if msi_credentials:
        self.log('Retrieved credentials from MSI.')
        return msi_credentials
    try:
        if HAS_AZURE_CLI_CORE:
            self.log('Retrieving credentials from AzureCLI profile')
        cli_credentials = self._get_azure_cli_credentials()
        return cli_credentials
    except CLIError as ce:
        self.log('Error getting AzureCLI profile credentials - {0}'.format(ce))
    return None