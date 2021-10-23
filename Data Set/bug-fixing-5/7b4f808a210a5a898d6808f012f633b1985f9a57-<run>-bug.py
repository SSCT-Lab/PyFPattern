def run(self, terms, variables=None, **kwargs):
    terms = self._lookup_variables(terms)
    my_list = terms[:]
    if (len(my_list) == 0):
        raise AnsibleError('with_together requires at least one element in each list')
    return [self._flatten(x) for x in izip_longest(*my_list, fillvalue=None)]