def get(self, tries=3, sleep=15, always_raise_on=None):
    '\n        Get instance connection information.\n        :type tries: int\n        :type sleep: int\n        :type always_raise_on: list[int] | None\n        :rtype: InstanceConnection\n        '
    if (not self.started):
        display.info(('Skipping invalid %s/%s instance %s.' % (self.platform, self.version, self.instance_id)), verbosity=1)
        return None
    if (not always_raise_on):
        always_raise_on = []
    if (self.connection and self.connection.running):
        return self.connection
    while True:
        tries -= 1
        response = self.client.get(self._uri)
        if (response.status_code == 200):
            break
        error = self._create_http_error(response)
        if ((not tries) or (response.status_code in always_raise_on)):
            raise error
        display.warning(('%s. Trying again after %d seconds.' % (error, sleep)))
        time.sleep(sleep)
    if self.args.explain:
        self.connection = InstanceConnection(running=True, hostname='cloud.example.com', port=(self.port or 12345), username='username', password=('password' if (self.platform == 'windows') else None))
    else:
        response_json = response.json()
        status = response_json['status']
        con = response_json['connection']
        self.connection = InstanceConnection(running=(status == 'running'), hostname=con['hostname'], port=int(con.get('port', self.port)), username=con['username'], password=con.get('password'))
        if self.connection.password:
            display.sensitive.add(str(self.connection.password))
    status = ('running' if self.connection.running else 'starting')
    display.info(('Status update: %s/%s on instance %s is %s.' % (self.platform, self.version, self.instance_id, status)), verbosity=1)
    return self.connection