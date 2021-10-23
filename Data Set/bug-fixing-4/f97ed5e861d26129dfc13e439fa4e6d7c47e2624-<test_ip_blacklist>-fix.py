@stub_blacklist(['127.0.0.1', '::1', '10.0.0.0/8'])
def test_ip_blacklist(self):
    with pytest.raises(SuspiciousOperation):
        http.safe_urlopen('http://127.0.0.1')
    with pytest.raises(SuspiciousOperation):
        http.safe_urlopen('http://10.0.0.10')
    with pytest.raises(SuspiciousOperation):
        http.safe_urlopen('http://2130706433')
    with pytest.raises(SuspiciousOperation):
        http.safe_urlopen('http://[::1]')