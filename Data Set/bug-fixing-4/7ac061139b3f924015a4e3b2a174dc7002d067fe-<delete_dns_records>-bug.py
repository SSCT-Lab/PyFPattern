def delete_dns_records(self, **kwargs):
    params = {
        
    }
    for param in ['port', 'proto', 'service', 'solo', 'type', 'record', 'value', 'weight', 'zone']:
        if (param in kwargs):
            params[param] = kwargs[param]
        else:
            params[param] = getattr(self, param)
    records = []
    content = params['value']
    search_record = params['record']
    if (params['type'] == 'SRV'):
        content = ((((str(params['weight']) + '\t') + str(params['port'])) + '\t') + params['value'])
        search_record = ((((params['service'] + '.') + params['proto']) + '.') + params['record'])
    if params['solo']:
        search_value = None
    else:
        search_value = content
    records = self.get_dns_records(params['zone'], params['type'], search_record, search_value)
    for rr in records:
        if params['solo']:
            if (not ((rr['type'] == params['type']) and (rr['name'] == search_record) and (rr['content'] == content))):
                self.changed = True
                if (not self.module.check_mode):
                    (result, info) = self._cf_api_call('/zones/{0}/dns_records/{1}'.format(rr['zone_id'], rr['id']), 'DELETE')
        else:
            self.changed = True
            if (not self.module.check_mode):
                (result, info) = self._cf_api_call('/zones/{0}/dns_records/{1}'.format(rr['zone_id'], rr['id']), 'DELETE')
    return self.changed