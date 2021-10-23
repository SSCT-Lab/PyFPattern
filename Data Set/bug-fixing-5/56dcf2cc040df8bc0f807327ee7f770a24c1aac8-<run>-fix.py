def run(self, terms, variables, **kwargs):
    results = []
    for term in terms:
        try:
            self.reset()
            try:
                if (not self.parse_simple_args(term)):
                    self.parse_kv_args(parse_kv(term))
            except AnsibleError:
                raise
            except Exception as e:
                raise AnsibleError(('unknown error parsing with_sequence arguments: %r. Error was: %s' % (term, e)))
            self.sanity_check()
            if (self.stride != 0):
                results.extend(self.generate_sequence())
        except AnsibleError:
            raise
        except Exception as e:
            raise AnsibleError(('unknown error generating sequence: %s' % e))
    return results