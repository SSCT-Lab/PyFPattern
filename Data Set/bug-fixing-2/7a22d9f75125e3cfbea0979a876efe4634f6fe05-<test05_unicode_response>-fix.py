

@mock.patch('socket.gethostbyname')
def test05_unicode_response(self, gethostbyname):
    'GeoIP strings should be properly encoded (#16553).'
    gethostbyname.return_value = '194.27.42.76'
    g = GeoIP2()
    d = g.city('nigde.edu.tr')
    self.assertEqual('Niğde', d['city'])
    d = g.country('200.26.205.1')
    self.assertIn(d['country_name'], ('Curaçao', 'Curacao'))
