def test_ip_blacklist(self):
    http.DISALLOWED_IPS = set([ipaddress.ip_network('127.0.0.1'), ipaddress.ip_network('::1'), ipaddress.ip_network('10.0.0.0/8')])
    with pytest.raises(SuspiciousOperation):
        http.safe_urlopen('http://127.0.0.1')
    with pytest.raises(SuspiciousOperation):
        http.safe_urlopen('http://10.0.0.10')
    with pytest.raises(SuspiciousOperation):
        http.safe_urlopen('http://2130706433')
    with pytest.raises(SuspiciousOperation):
        http.safe_urlopen('http://[::1]')