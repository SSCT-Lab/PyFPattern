def ensure_dns_record(self, **kwargs):
    params = {
        
    }
    for param in ['port', 'priority', 'proto', 'proxied', 'service', 'ttl', 'type', 'record', 'value', 'weight', 'zone']:
        if (param in kwargs):
            params[param] = kwargs[param]
        else:
            params[param] = getattr(self, param)
    search_value = params['value']
    search_record = params['record']
    new_record = None
    if ((params['type'] is None) or (params['record'] is None)):
        self.module.fail_json(msg='You must provide a type and a record to create a new record')
    if (params['type'] in ['A', 'AAAA', 'CNAME', 'TXT', 'MX', 'NS', 'SPF']):
        if (not params['value']):
            self.module.fail_json(msg='You must provide a non-empty value to create this record type')
        if (params['type'] == 'CNAME'):
            search_value = None
        new_record = {
            'type': params['type'],
            'name': params['record'],
            'content': params['value'],
            'ttl': params['ttl'],
        }
    if (params['type'] in ['A', 'AAAA', 'CNAME']):
        new_record['proxied'] = params['proxied']
    if (params['type'] == 'MX'):
        for attr in [params['priority'], params['value']]:
            if ((attr is None) or (attr == '')):
                self.module.fail_json(msg='You must provide priority and a value to create this record type')
        new_record = {
            'type': params['type'],
            'name': params['record'],
            'content': params['value'],
            'priority': params['priority'],
            'ttl': params['ttl'],
        }
    if (params['type'] == 'SRV'):
        for attr in [params['port'], params['priority'], params['proto'], params['service'], params['weight'], params['value']]:
            if ((attr is None) or (attr == '')):
                self.module.fail_json(msg='You must provide port, priority, proto, service, weight and a value to create this record type')
        srv_data = {
            'target': params['value'],
            'port': params['port'],
            'weight': params['weight'],
            'priority': params['priority'],
            'name': params['record'][:(- len(('.' + params['zone'])))],
            'proto': params['proto'],
            'service': params['service'],
        }
        new_record = {
            'type': params['type'],
            'ttl': params['ttl'],
            'data': srv_data,
        }
        search_value = ((((str(params['weight']) + '\t') + str(params['port'])) + '\t') + params['value'])
        search_record = ((((params['service'] + '.') + params['proto']) + '.') + params['record'])
    zone_id = self._get_zone_id(params['zone'])
    records = self.get_dns_records(params['zone'], params['type'], search_record, search_value)
    if (len(records) > 1):
        self.module.fail_json(msg='More than one record already exists for the given attributes. That should be impossible, please open an issue!')
    if (len(records) == 1):
        cur_record = records[0]
        do_update = False
        if ((params['ttl'] is not None) and (cur_record['ttl'] != params['ttl'])):
            do_update = True
        if ((params['priority'] is not None) and ('priority' in cur_record) and (cur_record['priority'] != params['priority'])):
            do_update = True
        if (('data' in new_record) and ('data' in cur_record)):
            if ((cur_record['data'] > new_record['data']) - (cur_record['data'] < new_record['data'])):
                do_update = True
        if ((type == 'CNAME') and (cur_record['content'] != new_record['content'])):
            do_update = True
        if do_update:
            if self.module.check_mode:
                result = new_record
            else:
                (result, info) = self._cf_api_call('/zones/{0}/dns_records/{1}'.format(zone_id, records[0]['id']), 'PUT', new_record)
            self.changed = True
            return (result, self.changed)
        else:
            return (records, self.changed)
    if self.module.check_mode:
        result = new_record
    else:
        (result, info) = self._cf_api_call('/zones/{0}/dns_records'.format(zone_id), 'POST', new_record)
    self.changed = True
    return (result, self.changed)