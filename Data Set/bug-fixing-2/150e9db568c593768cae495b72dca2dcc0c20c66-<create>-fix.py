

def create(self):
    '\n        :return:\n        '
    self.url = '{0}/{1}/e/{2}/{3}/{4}'.format(self.base_url, urllib_parse.quote(self.vhost, safe=''), urllib_parse.quote(self.name, safe=''), self.destination_type, urllib_parse.quote(self.destination, safe=''))
    self.api_result = self.request.post(self.url, auth=self.authentication, verify=self.verify, cert=(self.cert, self.key), headers={
        'content-type': 'application/json',
    }, data=json.dumps({
        'routing_key': self.routing_key,
        'arguments': self.arguments,
    }))
