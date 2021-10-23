def read_current_from_device(self):
    uri = 'https://{0}:{1}/mgmt/tm/sys/file/ssl-cert/{2}'.format(self.client.provider['server'], self.client.provider['server_port'], transform_name(self.want.partition, self.want.filename))
    query = '?expandSubcollections=true'
    resp = self.client.api.get((uri + query))
    try:
        response = resp.json()
    except ValueError as ex:
        raise F5ModuleError(str(ex))
    if (('code' in response) and (response['code'] == 400)):
        if ('message' in response):
            raise F5ModuleError(response['message'])
        else:
            raise F5ModuleError(resp.content)
    return ApiParameters(params=response)