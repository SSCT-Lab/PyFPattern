def save_config(self):
    self.execute(['copy running-config startup-config'])