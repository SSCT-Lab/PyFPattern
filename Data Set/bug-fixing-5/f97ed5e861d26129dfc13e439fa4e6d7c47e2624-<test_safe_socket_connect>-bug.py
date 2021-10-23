def test_safe_socket_connect(self):
    http.DISALLOWED_IPS = set([ipaddress.ip_network('127.0.0.1')])
    with pytest.raises(SuspiciousOperation):
        http.safe_socket_connect(('127.0.0.1', 80))