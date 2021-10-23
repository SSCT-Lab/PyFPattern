def is_deployed(self):
    uri = 'https://{0}:{1}/mgmt/tm/vcmp/guest/{2}/stats'.format(self.client.provider['server'], self.client.provider['server_port'], self.want.name)
    resp = self.client.api.get(uri)
    try:
        response = resp.json()
    except ValueError:
        return False
    if (('code' in response) and (response['code'] == 400)):
        if ('message' in response):
            raise F5ModuleError(response['message'])
        else:
            raise F5ModuleError(resp.content)
    if ((resp.status == 404) or (('code' in response) and (response['code'] == 404))):
        return False
    result = parseStats(response)
    if ('stats' in result):
        if (result['requestedState']['description'] == 'deployed'):
            if (result['vmStatus']['description'] == 'running'):
                return True
    return False