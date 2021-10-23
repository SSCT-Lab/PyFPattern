def exists(self):
    uri = 'https://{0}:{1}/mgmt/tm/sys/file/ssl-cert/{2}'.format(self.client.provider['server'], self.client.provider['server_port'], transform_name(self.want.partition, self.want.filename))
    resp = self.client.api.get(uri)
    try:
        response = resp.json()
    except ValueError:
        return False
    if ((resp.status == 404) or (('code' in response) and (response['code'] == 404))):
        return False
    return True