@pytest.mark.skipif((platform.system() == 'Darwin'), reason='macOS is always broken, see comment in sentry/http.py')
def test_garbage_ip(self):
    http.DISALLOWED_IPS = set([ipaddress.ip_network('127.0.0.1')])
    with pytest.raises(SuspiciousOperation):
        http.safe_urlopen('http://0177.0000.0000.0001')