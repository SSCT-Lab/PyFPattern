def set_query_parameters(self):
    '\n        Return dictionary of query parameters and\n        :return:\n        '
    query = {
        'policy-name': self.parameters['name'],
        'vserver': self.parameters['vserver'],
    }
    if self.parameters.get('rule_index'):
        query['rule-index'] = self.parameters['rule_index']
    elif self.parameters.get('client_match'):
        query['client-match'] = self.parameters['client_match']
    else:
        self.module.fail_json(msg='Need to specify at least one of the rule_index and client_match option.')
    attributes = {
        'query': {
            'export-rule-info': query,
        },
    }
    return attributes