

def test_smart_urlquote(self):
    items = (('http://öäü.com/', 'http://xn--4ca9at.com/'), ('http://öäü.com/öäü/', 'http://xn--4ca9at.com/%C3%B6%C3%A4%C3%BC/'), ('http://example.com/path/öäü/', 'http://example.com/path/%C3%B6%C3%A4%C3%BC/'), ('http://example.com/%C3%B6/ä/', 'http://example.com/%C3%B6/%C3%A4/'), ('http://example.com/?x=1&y=2+3&z=', 'http://example.com/?x=1&y=2+3&z='), ('http://example.com/?x=<>"\'', 'http://example.com/?x=%3C%3E%22%27'), ('http://example.com/?q=http://example.com/?x=1%26q=django', 'http://example.com/?q=http%3A%2F%2Fexample.com%2F%3Fx%3D1%26q%3Ddjango'), ('http://example.com/?q=http%3A%2F%2Fexample.com%2F%3Fx%3D1%26q%3Ddjango', 'http://example.com/?q=http%3A%2F%2Fexample.com%2F%3Fx%3D1%26q%3Ddjango'), ('http://.www.f oo.bar/', 'http://.www.f%20oo.bar/'))
    for (value, output) in items:
        with self.subTest(value=value, output=output):
            self.assertEqual(smart_urlquote(value), output)
