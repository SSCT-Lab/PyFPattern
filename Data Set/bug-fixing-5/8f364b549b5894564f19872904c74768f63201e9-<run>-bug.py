def run(self, terms, variables, **kwargs):
    if (not isinstance(terms, list)):
        raise AnsibleError('with_indexed_items expects a list')
    items = self._flatten(terms)
    return zip(range(len(items)), items)