def __init__(self):
    super(InventoryModule, self).__init__()
    self.token = self.get_option('oauth_token')
    self.config_data = None