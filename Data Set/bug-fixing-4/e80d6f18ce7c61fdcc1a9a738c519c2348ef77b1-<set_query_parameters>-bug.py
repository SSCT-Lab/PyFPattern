def set_query_parameters(self):
    '\n        Return dictionary of query parameters and\n        :return:\n        '
    query = {
        'policy-name': self.parameters['name'],
        'vserver': self.parameters['vserver'],
    }
    if self.parameters.get('rule_index'):
        query['rule-index'] = self.parameters['rule_index']
    else:
        if self.parameters.get('ro_rule'):
            query['ro-rule'] = {
                'security-flavor': self.parameters['ro_rule'],
            }
        if self.parameters.get('rw_rule'):
            query['rw-rule'] = {
                'security-flavor': self.parameters['rw_rule'],
            }
        if self.parameters.get('protocol'):
            query['protocol'] = {
                'security-flavor': self.parameters['protocol'],
            }
        if self.parameters.get('client_match'):
            query['client-match'] = self.parameters['client_match']
    attributes = {
        'query': {
            'export-rule-info': query,
        },
    }
    return attributes