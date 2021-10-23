@stub_blacklist(['127.0.0.1'])
def test_safe_socket_connect(self):
    with pytest.raises(SuspiciousOperation):
        http.safe_socket_connect(('127.0.0.1', 80))