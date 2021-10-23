@pytest.mark.skipif((platform.system() == 'Darwin'), reason='macOS is always broken, see comment in sentry/http.py')
@stub_blacklist(['127.0.0.1'])
def test_garbage_ip(self):
    with pytest.raises(SuspiciousOperation):
        http.safe_urlopen('http://0177.0000.0000.0001')