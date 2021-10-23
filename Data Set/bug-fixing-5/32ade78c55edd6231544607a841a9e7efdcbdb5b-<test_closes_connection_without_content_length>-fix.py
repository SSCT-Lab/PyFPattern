@override_settings(MIDDLEWARE=[])
def test_closes_connection_without_content_length(self):
    "\n        The server doesn't support keep-alive because Python's http.server\n        module that it uses hangs if a Content-Length header isn't set (for\n        example, if CommonMiddleware isn't enabled or if the response is a\n        StreamingHttpResponse) (#28440 / https://bugs.python.org/issue31076).\n        "
    conn = HTTPConnection(LiveServerViews.server_thread.host, LiveServerViews.server_thread.port, timeout=1)
    try:
        conn.request('GET', '/example_view/', headers={
            'Connection': 'keep-alive',
        })
        response = conn.getresponse().read()
        conn.request('GET', '/example_view/', headers={
            'Connection': 'close',
        })
        with self.assertRaises((RemoteDisconnected, ConnectionResetError)):
            try:
                conn.getresponse()
            except ConnectionAbortedError:
                if (sys.platform == 'win32'):
                    self.skipTest('Ignore nondeterministic failure on Windows.')
    finally:
        conn.close()
    self.assertEqual(response, b'example view')