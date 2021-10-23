def run(self, terms, variables=None, **kwargs):
    if (not isinstance(terms, collections.Mapping)):
        raise AnsibleError('with_dict expects a dict')
    return self._flatten_hash_to_list(terms)