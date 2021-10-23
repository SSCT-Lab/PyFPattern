def edit_domain_record(self, record):
    params = {
        'name': '@',
        'data': self.module.params.get('ip'),
    }
    resp = self.put(('domains/%s/records/%s' % (self.domain_name, record['id'])), data=params)
    (status, json) = self.jsonify(resp)
    return json['domain_record']