

def run(self, terms, variables=None, **kwargs):
    if (not isinstance(terms, list)):
        terms = [terms]
    results = []
    for term in terms:
        if (not isinstance(term, collections.Mapping)):
            raise AnsibleError('with_dict expects a dict')
        results.extend(self._flatten_hash_to_list(term))
    return results
