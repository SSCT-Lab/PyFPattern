def _get_credentials(self):
    'Wait for the CloudStack simulator to return credentials.\n        :rtype: dict[str, str]\n        '
    client = HttpClient(self.args, always=True)
    endpoint = ('%s/admin.json' % self.endpoint)
    for _ in range(1, 30):
        display.info(('Waiting for CloudStack credentials: %s' % endpoint), verbosity=1)
        response = client.get(endpoint)
        if (response.status_code == 200):
            return response.json()
        time.sleep(30)
    raise ApplicationError('Timeout waiting for CloudStack credentials.')