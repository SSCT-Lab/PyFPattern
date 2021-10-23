def create_bios_config_job(self):
    result = {
        
    }
    key = 'Bios'
    jobs = 'Jobs'
    response = self.get_request((self.root_uri + self.systems_uri))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
    bios_uri = data[key]['@odata.id']
    response = self.get_request((self.root_uri + bios_uri))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
    set_bios_attr_uri = data['@Redfish.Settings']['SettingsObject']['@odata.id']
    payload = {
        'TargetSettingsURI': set_bios_attr_uri,
        'RebootJobType': 'PowerCycle',
    }
    response = self.post_request((((self.root_uri + self.manager_uri) + '/') + jobs), payload, HEADERS)
    if (response['ret'] is False):
        return response
    response_output = response['resp'].__dict__
    job_id = response_output['headers']['Location']
    job_id = re.search('JID_.+', job_id).group()
    return {
        'ret': True,
        'msg': 'Config job created',
        'job_id': job_id,
    }