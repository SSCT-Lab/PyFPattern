

def save_config(self, **kwargs):
    try:
        self.execute(['copy running-config startup-config'], output='text')
    except TypeError:
        self.execute(['copy running-config startup-config'])
