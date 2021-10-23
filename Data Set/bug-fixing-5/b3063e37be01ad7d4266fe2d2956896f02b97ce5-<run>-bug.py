def run(self, terms, variables=None, **kwargs):
    if (not HAS_CONSUL):
        raise AnsibleError('python-consul is required for consul_kv lookup. see http://python-consul.readthedocs.org/en/latest/#installation')
    values = []
    try:
        for term in terms:
            params = self.parse_params(term)
            try:
                url = os.environ['ANSIBLE_CONSUL_URL']
                validate_certs = (os.environ['ANSIBLE_CONSUL_VALIDATE_CERTS'] or True)
                client_cert = (os.environ['ANSIBLE_CONSUL_CLIENT_CERT'] or None)
                u = urlparse(url)
                consul_api = consul.Consul(host=u.hostname, port=u.port, scheme=u.scheme, verify=validate_certs, cert=client_cert)
            except KeyError:
                port = kwargs.get('port', '8500')
                host = kwargs.get('host', 'localhost')
                scheme = kwargs.get('scheme', 'http')
                validate_certs = kwargs.get('validate_certs', True)
                client_cert = kwargs.get('client_cert', None)
                consul_api = consul.Consul(host=host, port=port, scheme=scheme, verify=validate_certs, cert=client_cert)
            results = consul_api.kv.get(params['key'], token=params['token'], index=params['index'], recurse=params['recurse'])
            if results[1]:
                if isinstance(results[1], list):
                    for r in results[1]:
                        values.append(r['Value'])
                else:
                    values.append(results[1]['Value'])
    except Exception as e:
        raise AnsibleError(("Error locating '%s' in kv store. Error was %s" % (term, e)))
    return values