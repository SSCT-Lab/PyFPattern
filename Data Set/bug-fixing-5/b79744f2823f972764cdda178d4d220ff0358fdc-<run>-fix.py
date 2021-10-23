def run(self, terms, inject=None, **kwargs):
    ret = terms
    if terms:
        try:
            ret = [random.choice(terms)]
        except Exception as e:
            raise AnsibleError(('Unable to choose random term: %s' % to_native(e)))
    return ret