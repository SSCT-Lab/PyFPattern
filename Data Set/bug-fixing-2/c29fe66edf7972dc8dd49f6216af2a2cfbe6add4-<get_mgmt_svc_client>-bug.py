

def get_mgmt_svc_client(self, client_type, base_url=None, api_version=None):
    self.log('Getting management service client {0}'.format(client_type.__name__))
    self.check_client_version(client_type)
    client_argspec = inspect.getargspec(client_type.__init__)
    client_kwargs = dict(credentials=self.azure_credentials, subscription_id=self.subscription_id, base_url=base_url)
    api_profile_dict = {
        
    }
    if self.api_profile:
        api_profile_dict = self.get_api_profile(client_type.__name__, self.api_profile)
    if (not base_url):
        base_url = self._cloud_environment.endpoints.resource_manager
    if (api_profile_dict and ('profile' in client_argspec.args)):
        client_kwargs['profile'] = api_profile_dict
    if ('api_version' in client_argspec.args):
        profile_default_version = api_profile_dict.get('default_api_version', None)
        if (api_version or profile_default_version):
            client_kwargs['api_version'] = (api_version or profile_default_version)
            if ('profile' in client_kwargs):
                client_kwargs.pop('profile')
    client = client_type(**client_kwargs)
    try:
        getattr(client, 'models')
    except AttributeError:

        def _ansible_get_models(self, *arg, **kwarg):
            return self._ansible_models
        setattr(client, '_ansible_models', importlib.import_module(client_type.__module__).models)
        client.models = types.MethodType(_ansible_get_models, client)
    client.config.add_user_agent(ANSIBLE_USER_AGENT)
    if (CLOUDSHELL_USER_AGENT_KEY in os.environ):
        client.config.add_user_agent(os.environ[CLOUDSHELL_USER_AGENT_KEY])
    if (VSCODEEXT_USER_AGENT_KEY in os.environ):
        client.config.add_user_agent(os.environ[VSCODEEXT_USER_AGENT_KEY])
    if (self._cert_validation_mode == 'ignore'):
        client.config.session_configuration_callback = self._validation_ignore_callback
    return client
