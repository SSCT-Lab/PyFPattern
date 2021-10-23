def update_on_device(self):
    content = StringIO(self.want.content)
    self.upload_file_to_device(content, self.want.filename)
    params = self.changes.api_params()
    uri = 'https://{0}:{1}/mgmt/tm/sys/file/ssl-cert/{2}'.format(self.client.provider['server'], self.client.provider['server_port'], transform_name(self.want.partition, self.want.filename))
    resp = self.client.api.put(uri, json=params)
    try:
        response = resp.json()
    except ValueError as ex:
        raise F5ModuleError(str(ex))
    if (('code' in response) and (response['code'] == 400)):
        if ('message' in response):
            raise F5ModuleError(response['message'])
        else:
            raise F5ModuleError(resp.content)