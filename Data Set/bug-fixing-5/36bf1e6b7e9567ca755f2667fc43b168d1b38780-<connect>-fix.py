def connect(self, port=None):
    if (not HAVE_FUNC):
        raise AnsibleError('func is not installed')
    self.client = fc.Client(self.host)
    return self