def __init__(self, module):
    self.module = module
    self.config = module.params.get('config')
    self.name = module.params.get('name')
    self.password = module.params.get('password')
    self.state = module.params.get('state')
    self.enabled = module.params.get('enabled')
    self.token = module.params.get('token')
    self.user = module.params.get('user')
    self.jenkins_url = module.params.get('url')
    self.server = self.get_jenkins_connection()
    self.result = {
        'changed': False,
        'url': self.jenkins_url,
        'name': self.name,
        'user': self.user,
        'state': self.state,
        'diff': {
            'before': '',
            'after': '',
        },
    }
    self.EXCL_STATE = 'excluded state'