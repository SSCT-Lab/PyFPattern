def call(self):
    self._validate()
    self._delete_grant()
    self._create_token()
    return self.token