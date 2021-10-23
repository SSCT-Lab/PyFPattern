def __init__(self):
    super(CallbackModule, self).__init__()
    self.items = defaultdict(list)
    self.start_time = int(time.time())
    if HAS_REQUESTS:
        requests_major = int(requests.__version__.split('.')[0])
        if (requests_major >= 2):
            self.ssl_verify = self._ssl_verify()
        else:
            self._disable_plugin('The `requests` python module is too old.')
    else:
        self._disable_plugin('The `requests` python module is not installed.')
    if self.FOREMAN_URL.startswith('https://'):
        if (not os.path.exists(self.FOREMAN_SSL_CERT[0])):
            self._disable_plugin(('FOREMAN_SSL_CERT %s not found.' % self.FOREMAN_SSL_CERT[0]))
        if (not os.path.exists(self.FOREMAN_SSL_CERT[1])):
            self._disable_plugin(('FOREMAN_SSL_KEY %s not found.' % self.FOREMAN_SSL_CERT[1]))