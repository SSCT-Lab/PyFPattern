def __init__(self, module):
    '\n        :param module:\n        '
    self.module = module
    self.name = self.module.params['name']
    self.login_user = self.module.params['login_user']
    self.login_password = self.module.params['login_password']
    self.login_host = self.module.params['login_host']
    self.login_port = self.module.params['login_port']
    self.vhost = self.module.params['vhost']
    self.destination = self.module.params['destination']
    self.destination_type = ('q' if (self.module.params['destination_type'] == 'queue') else 'e')
    self.routing_key = self.module.params['routing_key']
    self.arguments = self.module.params['arguments']
    self.base_url = 'http://{0}:{1}/api/bindings'.format(self.login_host, self.login_port)
    self.url = '{0}/{1}/e/{2}/{3}/{4}/{5}'.format(self.base_url, urllib_parse.quote(self.vhost, safe=''), urllib_parse.quote(self.name, safe=''), self.destination_type, urllib_parse.quote(self.destination, safe=''), urllib_parse.quote(self.routing_key))
    self.result = {
        'changed': False,
        'name': self.module.params['name'],
    }
    self.authentication = (self.login_user, self.login_password)
    self.request = requests
    self.http_check_states = {
        200: True,
        404: False,
    }
    self.http_actionable_states = {
        201: True,
        204: True,
    }
    self.api_result = self.request.get(self.url, auth=self.authentication)