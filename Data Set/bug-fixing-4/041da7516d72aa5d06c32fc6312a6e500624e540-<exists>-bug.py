def exists(self):
    uri = 'https://{0}:{1}/mgmt/tm/gtm/server/{2}/virtual-servers/{3}'.format(self.client.provider['server'], self.client.provider['server_port'], transform_name(self.want.partition, self.want.server_name), self.want.name)
    resp = self.client.api.get(uri)
    try:
        response = resp.json()
    except ValueError:
        return False
    if ((resp.status == 404) or (('code' in response) and (response['code'] == 404))):
        return False
    return True