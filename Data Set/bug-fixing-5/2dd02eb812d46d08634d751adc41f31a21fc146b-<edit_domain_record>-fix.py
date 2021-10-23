def edit_domain_record(self):
    params = {
        'name': self.domain_name,
    }
    resp = self.put(('domains/%s/records/%s' % (self.domain_name, self.domain_id)), data=params)
    (status, json) = self.jsonify(resp)
    return json['domain_record']