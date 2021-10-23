def create_on_device(self):
    params = self.changes.api_params()
    content = StringIO(self.want.content)
    self.upload_file_to_device(content, self.want.key_filename)
    params['name'] = self.want.key_filename
    params['partition'] = self.want.partition
    uri = 'https://{0}:{1}/mgmt/tm/sys/file/ssl-key/'.format(self.client.provider['server'], self.client.provider['server_port'])
    resp = self.client.api.post(uri, json=params)
    try:
        response = resp.json()
    except ValueError as ex:
        raise F5ModuleError(str(ex))
    if (('code' in response) and (response['code'] in [400, 403])):
        if ('message' in response):
            raise F5ModuleError(response['message'])
        else:
            raise F5ModuleError(resp.content)