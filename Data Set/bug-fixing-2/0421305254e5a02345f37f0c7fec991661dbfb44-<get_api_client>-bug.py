

def get_api_client(self, **auth_params):
    auth_args = AUTH_ARG_SPEC.keys()
    auth_params = (auth_params or getattr(self, 'params', {
        
    }))
    auth = copy.deepcopy(auth_params)
    configuration = kubernetes.client.Configuration()
    for (key, value) in iteritems(auth_params):
        if ((key in auth_args) and (value is not None)):
            if (key == 'api_key'):
                setattr(configuration, key, {
                    'authorization': 'Bearer {0}'.format(value),
                })
            else:
                setattr(configuration, key, value)
        elif ((key in auth_args) and (value is None)):
            env_value = os.getenv('K8S_AUTH_{0}'.format(key.upper()), None)
            if (env_value is not None):
                setattr(configuration, key, env_value)
                auth[key] = env_value
    kubernetes.client.Configuration.set_default(configuration)
    if (auth.get('username') and auth.get('password') and auth.get('host')):
        auth_method = 'params'
    elif (auth.get('api_key') and auth.get('host')):
        auth_method = 'params'
    elif (auth.get('kubeconfig') or auth.get('context')):
        auth_method = 'file'
    else:
        auth_method = 'default'
    if (auth_method == 'default'):
        try:
            kubernetes.config.load_incluster_config()
            return DynamicClient(kubernetes.client.ApiClient())
        except kubernetes.config.ConfigException:
            return DynamicClient(self.client_from_kubeconfig(auth.get('kubeconfig'), auth.get('context')))
    if (auth_method == 'file'):
        return DynamicClient(self.client_from_kubeconfig(auth.get('kubeconfig'), auth.get('context')))
    if (auth_method == 'params'):
        return DynamicClient(kubernetes.client.ApiClient(configuration))
