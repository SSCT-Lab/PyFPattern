def initial_image_exists(self, image):
    uri = 'https://{0}:{1}/mgmt/tm/sys/software/images/'.format(self.client.provider['server'], self.client.provider['server_port'])
    resp = self.client.api.get(uri)
    try:
        response = resp.json()
    except ValueError:
        return False
    if ((resp.status == 404) or (('code' in response) and (response['code'] == 404))):
        return False
    for resource in response['items']:
        if resource['name'].startswith(image):
            return True
    return False