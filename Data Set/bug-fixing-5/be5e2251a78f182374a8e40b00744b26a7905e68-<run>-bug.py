def run(self, terms, variables, **kwargs):
    if (not CREDSTASH_INSTALLED):
        raise AnsibleError('The credstash lookup plugin requires credstash to be installed.')
    ret = []
    for term in terms:
        try:
            version = kwargs.pop('version', '')
            region = kwargs.pop('region', None)
            table = kwargs.pop('table', 'credential-store')
            val = credstash.getSecret(term, version, region, table, context=kwargs)
        except credstash.ItemNotFound:
            raise AnsibleError('Key {0} not found'.format(term))
        except Exception as e:
            raise AnsibleError('Encountered exception while fetching {0}: {1}'.format(term, e.message))
        ret.append(val)
    return ret