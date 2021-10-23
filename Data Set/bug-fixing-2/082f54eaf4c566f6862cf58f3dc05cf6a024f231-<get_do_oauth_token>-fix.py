

def get_do_oauth_token(self):
    self.oauth_token = (self.module.params.get('oauth_token') or self.module.params.get('api_token') or os.environ.get('DO_API_TOKEN') or os.environ.get('DO_API_KEY') or os.environ.get('OAUTH_TOKEN'))
    if (self.oauth_token is None):
        self.module.fail_json(msg='Unable to load api key: oauth_token')
