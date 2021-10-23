

def call(self):
    self._validate()
    self._create_token()
    self._delete_grant()
    return self.token
