

def __init__(self, base_url, shared_secret):
    self.base_url = base_url
    self.shared_secret = shared_secret
    super(JiraApiClient, self).__init__(verify_ssl=False)
