

def get_do_oauth_token(self):
    try:
        self.oauth_token = (self.module.params['oauth_token'] or self.module.params['api_token'] or os.environ['DO_API_TOKEN'] or os.environ['DO_API_KEY'] or os.environ['OAUTH_TOKEN'])
    except KeyError as e:
        self.module.fail_json(msg=('Unable to load %s' % e.message))
