

def get_allowed_origins(self):
    if self.application:
        return self.application.get_allowed_origins()
    return ()
