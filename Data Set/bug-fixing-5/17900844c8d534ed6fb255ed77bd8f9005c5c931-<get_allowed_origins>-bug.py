def get_allowed_origins(self):
    if self.application:
        return self.key.get_allowed_origins()
    return ()