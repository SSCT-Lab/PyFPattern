def get_mgmt_svc_client(self, client_type, base_url=None, api_version=None):
    self.log('Getting management service client {0}'.format(client_type.__name__))
    self.check_client_version(client_type)
    if api_version:
        client = client_type(self.azure_credentials, self.subscription_id, api_version=api_version, base_url=base_url)
    else:
        client = client_type(self.azure_credentials, self.subscription_id, base_url=base_url)
    client.config.add_user_agent(ANSIBLE_USER_AGENT)
    if (CLOUDSHELL_USER_AGENT_KEY in os.environ):
        client.config.add_user_agent(os.environ[CLOUDSHELL_USER_AGENT_KEY])
    if (VSCODEEXT_USER_AGENT_KEY in os.environ):
        client.config.add_user_agent(os.environ[VSCODEEXT_USER_AGENT_KEY])
    return client