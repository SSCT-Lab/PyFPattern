def save_config(self, **kwargs):
    self.execute(['copy running-config startup-config'])