def exists(self):
    name = '{0}~{1}'.format(self.client.provider['user'], self.want.file)
    tpath = '/ts/var/rest/{0}'.format(name)
    params = dict(command='run', utilCmdArgs=tpath)
    uri = 'https://{0}:{1}/mgmt/tm/util/unix-ls/'.format(self.client.provider['server'], self.client.provider['server_port'])
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
    if ('commandResult' in response):
        if ('cannot access' in response['commandResult']):
            return False
        return True
    return False