@mock.patch('socket.gethostbyname')
def test05_unicode_response(self, gethostbyname):
    'GeoIP strings should be properly encoded (#16553).'
    gethostbyname.return_value = '191.252.51.69'
    g = GeoIP2()
    d = g.city('www.fasano.com.br')
    self.assertEqual(d['city'], 'São José dos Campos')
    d = g.country('200.26.205.1')
    self.assertIn(d['country_name'], ('Curaçao', 'Curacao'))